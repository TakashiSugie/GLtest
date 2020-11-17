FP2d_3d	Matchingで求めたnpy配列をIdxつけて３次元にする（x,y,Idx）
FP_2d→FP_3d
LR.py  Mを導出、FP_3d→M
Matching　dataset→FPimg,FP2d
createNewPly mesh1_2=M*mesh1を保存
libs 画像座標系→カメラ座標系に変換とかするライブラリ
makeNpy　画像座標系からカメラ座標系に変換しnpyに保存
mymkdir	shで必要なディレクトリを一通り作成
plyClass plyのClassを作成
plyFromNpy　Npyからmesh1,mesh2のPly作成
rendering rendering 今はintegrateしたやつをやってる
sameScaleRendering　３つのWindowでmesh1,mesh2,mesh1_2を表示
setVerts　renderingに用いるsetverts
variable　変数とかデータ名とかを書いてある
