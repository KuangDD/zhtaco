import numpy as np

def cut_data(data=()):
    tmp = np.sum(data, -1)
    flags = tmp >= (np.shape(data)[-1] / 10)
    segs = [[]]
    for i, f in enumerate(flags):
        if f:
            segs[-1].append(i)
        else:
            if segs[-1]:
                segs.append([])
    segs = [w for w in segs if w]
    # segs[1].extend(segs[2])
    # segs[1] = list(range(segs[1][0], segs[1][-1] + 1))
    # segs.pop(2)
    # print(len(segs))
    return segs




if __name__ == "__main__":
    # meldata = np.load(r"D:\git\tacotron\data\specs\ljspeech-mel-00002.npy")
    # specdata = np.load(r"D:\git\tacotron\data\specs\ljspeech-spec-00002.npy")
    # seg_lst = cut_data(meldata)
    # seg = list(range(seg_lst[0][0], seg_lst[-1][-1] + 1))
    # i = 7
    # np.save(fr"D:\git\tacotron\data\specs_v2\ljspeech-mel-0000{i}.npy", meldata[seg])
    # np.save(fr"D:\git\tacotron\data\specs_v2\ljspeech-spec-0000{i}.npy", specdata[seg])
    # print(f"{i}: {len(seg)}")
    from util.audio import inv_spectrogram, save_wav
    import os
    # filedir = r"D:\git\tacotron\data\specs_v2"
    # for filename in os.listdir(filedir):
    #     if not (filename.endswith(".npy") and filename.startswith("ljspeech-spec")):
    #         continue
    #     filepath = os.path.join(filedir, filename)
    #     data = np.load(filepath)
    #     data = np.concatenate((data, np.zeros_like(data)), 0)[:1025, :]
    #     wave = inv_spectrogram(data)
    #     save_wav(wave, os.path.splitext(filepath)[0] + ".wav")
    texts = open(r"D:\git\tacotron\data\specs_v2\metadata.csv", encoding="utf8").readlines()
    out_lst = []
    for i in range(1, 13):
        meldata = np.load(fr"D:\git\tacotron\data\specs_v2\ljspeech-mel-0000{i}.npy")
        specdata = np.load(fr"D:\git\tacotron\data\specs_v2\ljspeech-spec-0000{i}.npy")
        assert meldata.shape[0] == specdata.shape[0]
        out = fr"ljspeech-spec-0000{i}.npy|ljspeech-mel-0000{i}.npy|{meldata.shape[0]}|{texts[i - 1].strip()}"
        out_lst.append(out)
    with open(r"D:\git\tacotron\data\specs_v2\metadata_v2.csv", "wt", encoding="utf8") as fout:
        fout.write("\n".join(out_lst))





