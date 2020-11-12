u1, v1 = 0, 0
u2, v2 = 8, 8  # 0~8(uが→方向　vが下方向)
camNum1 = u1 * 9 + v1
camNum2 = u2 * 9 + v2
imgName1 = "input_Cam{:03}".format(camNum1)
imgName2 = "input_Cam{:03}".format(camNum2)
LFName = "antinous"
saveName = LFName + "_" + str(camNum1) + "_" + str(camNum2)
