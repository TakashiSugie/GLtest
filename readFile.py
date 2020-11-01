import re


def readCg(cgPath):
    patternList = ["focal_length_mm", "sensor_size_mm", "baseline_mm"]
    paraDict = {}
    with open(cgPath) as f:
        s = f.read()
        sLines = s.split("\n")
        for sLine in sLines:
            for pattern in patternList:
                if re.match(pattern, sLine):
                    sList = sLine.split()
                    paraDict[pattern] = float(sList[2])
    print(paraDict)
    return paraDict


def reTest():
    content = "hellow python"
    pattern = "python"
    # matchなら、先頭からピッタリする必要がある
    match_result = re.match(pattern, content)
    # searchなら、存在するだけで結果が出る
    search_result = re.search(pattern, content)
    if match_result:
        print("match_result:", match_result.group())
    else:
        print("match_result:none")
    # output:match_result:none

    if search_result:
        print("search_result:", search_result.group())
    else:
        print("search_result:none")
        # output:search_result: python


if __name__ == "__main__":
    cgPath = "/home/takashi/Desktop/dataset/lf_dataset/additional/tower/parameters.cfg"
    readCg(cgPath)


# reTest()
