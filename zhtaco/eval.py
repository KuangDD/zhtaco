import argparse
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import re
import json
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer

# sentences = [
#   # From July 8, 2017 New York Times:
#   'Scientists at the CERN laboratory say they have discovered a new particle.',
#   'There’s a way to measure the acute emotional intelligence that has never gone out of style.',
#   'President Trump met with other leaders at the Group of 20 conference.',
#   'The Senate\'s bill to repeal and replace the Affordable Care Act is now imperiled.',
#   # From Google's Tacotron example page:
#   'Generative adversarial network or variational auto-encoder.',
#   'The buses aren\'t the problem, they actually provide a solution.',
#   'Does the quick brown fox jump over the lazy dog?',
#   'Talib Kweli confirmed to AllHipHop that he will be releasing an album in the next year.',
# ]

sentences = '''1.生活岂能百般如意，
正因有了遗漏和缺憾，
我们才会有所追寻。
功成莫自得，
或许下一步就是陷阱；
败后勿卑微，
没有谁一直紧锁冬寒。
哪怕再平凡、平常、平庸，
都不能让梦想之地荒芜，
人生最可怕的，
不是你置身何处，
而是不知走向哪里。
2.人有很多面具，上班一个，下班一个；
工作一个，娱乐一个；
面对老板一个，面对客户一个；
面对同事一个，面对朋友一个……
能看到你不戴面具的人，是你最亲近最值得珍惜的人。
3.不管发生了什么事，
不要抱怨生命中的任何一天，
真正的大心境，在于放弃后的坦然，也在于放下后的无意。
人生反复，总会让我们悲喜交织，
遇时请珍重，路过请祝福。
拥有一个良好心态，生活就是一片艳阳天！'''.split('\n')


def get_output_base_path(checkpoint_path):
    base_dir = os.path.dirname(checkpoint_path)
    m = re.compile(r'.*?\.ckpt\-([0-9]+)').match(checkpoint_path)
    name = 'eval-%d' % int(m.group(1)) if m else 'eval'
    return os.path.join(base_dir, name)


def run_eval(args):
    print(hparams_debug_string())
    synth = Synthesizer()
    synth.load(args.checkpoint)
    base_path = get_output_base_path(args.checkpoint)
    os.makedirs(base_path, exist_ok=True)
    for i, text in enumerate(sentences, 1):
        wavname = '%s-%04d.wav' % (os.path.basename(base_path), i)
        path = os.path.join(base_path, wavname)
        print('Synthesizing: %s' % path)
        with open(path, 'wb') as f:
            f.write(synth.synthesize(text + '。。'))


def main():
    logdir = r'E:\data\logs\logs-biaobei-blank'
    step = 20000
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', default=os.path.join(logdir, 'model.ckpt-{}'.format(step)),
                        help='Path to model checkpoint')
    hp_path = os.path.join(os.path.join(logdir, 'hparams.json'))
    if os.path.exists(hp_path):
        hp = json.load(open(hp_path, encoding='utf8'))
        hp = ','.join('{}={}'.format(k, v) for k, v in hp.items())
    else:
        hp = ''
    parser.add_argument('--hparams', default=hp,
                        help='Hyperparameter overrides as a comma-separated list of name=value pairs')
    args = parser.parse_args()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    hparams.parse(args.hparams)
    run_eval(args)


if __name__ == '__main__':
    main()
