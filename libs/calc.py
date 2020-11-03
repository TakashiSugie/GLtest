def pix2m_disp(x, y, paraDict):
    if dispImg[x][y]:
        Z = float(beta * f_mm) / float((dispImg[x][y] * f_mm * s_mm + beta))
    else:
        print("zero!!")
        Z = 0
    X = float(x) * Z / f_pix
    Y = float(y) * Z / f_pix
    return X, Y, Z
