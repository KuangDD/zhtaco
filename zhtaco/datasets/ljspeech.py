from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os
from util import audio


def build_from_path(in_dir, out_dir, num_workers=1, tqdm=lambda x: x):
    '''Preprocesses the LJ Speech dataset from a given input path into a given output directory.

      Args:
        in_dir: The directory where you have downloaded the LJ Speech dataset
        out_dir: The directory to write the output into
        num_workers: Optional number of worker processes to parallelize across
        tqdm: You can optionally pass tqdm to get a nice progress bar

      Returns:
        A list of tuples describing the training examples. This should be written to train.txt
    '''

    # We use ProcessPoolExecutor to parallelize across processes. This is just an optimization and you
    # can omit it and just call _process_utterance on each input if you want.
    executor = ProcessPoolExecutor(max_workers=num_workers)
    futures = []
    index = 1
    with open(os.path.join(in_dir, 'metadata.csv'), encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')  # '|'
            wav_path = os.path.join(in_dir, 'wavs', '%s.wav' % parts[0])
            text = parts[1]  # [2]
            futures.append(executor.submit(partial(_process_utterance, out_dir, index, wav_path, text)))
            index += 1
    return [future.result() for future in tqdm(futures)]


def _process_utterance(out_dir, index, wav_path, text):
    '''Preprocesses a single utterance audio/text pair.

    This writes the mel and linear scale spectrograms to disk and returns a tuple to write
    to the train.txt file.

    Args:
      out_dir: The directory to write the spectrograms into
      index: The numeric index to use in the spectrogram filenames.
      wav_path: Path to the audio file containing the speech input
      text: The text spoken in the input audio file

    Returns:
      A (spectrogram_filename, mel_filename, n_frames, text) tuple to write to train.txt
    '''

    # Load the audio to a numpy array:
    wav = audio.load_wav(wav_path)

    # Compute the linear-scale spectrogram from the wav:
    spectrogram = audio.spectrogram(wav).astype(np.float32)
    n_frames = spectrogram.shape[1]

    # Compute a mel-scale spectrogram from the wav:
    mel_spectrogram = audio.melspectrogram(wav).astype(np.float32)

    # Write the spectrograms to disk:
    spectrogram_filename = 'ljspeech-spec-%05d.npy' % index
    mel_filename = 'ljspeech-mel-%05d.npy' % index
    np.save(os.path.join(out_dir, spectrogram_filename), spectrogram.T, allow_pickle=False)
    np.save(os.path.join(out_dir, mel_filename), mel_spectrogram.T, allow_pickle=False)

    # Return a tuple describing this training example:
    return (spectrogram_filename, mel_filename, n_frames, text)


if __name__ == "__main__":
    import json
    from tqdm import tqdm

    inpath = r"E:\data\xunfei\xinqing\xinqing_idx2text_split.json"
    idx_texts_dict = json.load(open(inpath, encoding="utf8"))
    idx_text_dict = {}
    for k, v in idx_texts_dict.items():
        for i, t in enumerate(v, 1):
            idx = f"{k}_{i}"
            idx_text_dict[idx] = t
    out_dir = r"E:\data\xunfei\xinqing\xinqing_split_specs"
    try:
        os.makedirs(out_dir)
    except FileExistsError:
        pass
    in_dir = r"E:\data\xunfei\xinqing\xinqing_split_wavs"
    fname_list = [w for w in os.listdir(in_dir)]
    fname_list_new = sorted(fname_list, key=lambda x: (int(x.split("_")[-2]), int(x.split("_")[-1].split(".")[0])))
    outpath = "_".join(out_dir.split("_")[:-1]) + "_meta.csv"
    with open(outpath, "wt", encoding="utf8") as fout:
        for i, fname in enumerate(tqdm(fname_list_new), 1):
            wav_path = os.path.join(in_dir, fname)
            segs = fname.split("_")
            b = segs[-1].split(".")[0]
            idx = f"{segs[-2]}_{b}"
            text = idx_text_dict[idx]
            (spectrogram_filename, mel_filename, n_frames, text) = _process_utterance(out_dir=out_dir, index=i,
                                                                                      wav_path=wav_path, text=text)
            fout.write("|".join((spectrogram_filename, mel_filename, str(n_frames), text)))
            fout.write("\n")
