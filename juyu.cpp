#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <GL/glut.h>
#include<iostream>
#include <opencv2/opencv.hpp>
#define WINDOW_NAME "3D-object"
using namespace std;
using namespace cv;
void init(void);
void glut_display(void);
void glut_keyboard(unsigned char key, int x, int y);
void glut_mouse(int button, int state, int x, int y);
void glut_motion(int x, int y); bool RightButtonOn = false;
void draw(void);
void draw2(void);
void draw3(void);
void draw4(void);
void draw5(void);
double Angle1 = 0.0;
double Angle2 = 0.0;
double Distance = 7.0;
bool LeftButtonOn = false;
Mat d_img;
Mat img=imread("med.png",1);
float ratio=0.001;
double minVal = 10;
double maxVal = 0.0;//minmaxlocにdoubleしか入らない
vector<string> split(string& input, char delimiter)//入力　何で区切るか　文字列の可変長配列
{
  istringstream stream(input);
  string field;
  vector<string> result;
  while (getline(stream, field, delimiter)) {
    result.push_back(field);
  }
  return result;
}

Mat dis2dep(void)
{
  ifstream ifs("medieval2_gt_depth.csv");//ここでifstreamクラスのインスタンスのifsにファイルの内容を全行格納　ファイル読み取り用のクラス他にもfopenとかfgetsも
  string line;
  Mat output=Mat::zeros(img.size(),CV_32FC1);
  for (int y = 0; y < img.rows; y++) {
    getline(ifs, line);//一行読み込んで文字列ラインに格納
    vector<string> strvec = split(line, ',');//strvecに配列のデータを一つずつ追加
    for (int x = 0; x < img.cols; x++) {
      output.at<float>(y,x) =stof(strvec.at(x));//この配列の・・番目の要素をfloatで取り出すよ 何番目の要素を strを数値と読み取り、floatに変換
    }
  }
  minMaxLoc(output, &minVal, &maxVal, NULL, NULL);
  output=(output-minVal)/(maxVal-minVal) * 255.0;//正規化　値としては入れることができるが勿論ここで出力したら白に発散
  output.convertTo( output, CV_8UC1 );//受け渡しのときにはイント型にする必要がある//四捨五入してる
  bitwise_not(output,output);  //depth大　つまり値が大きいほど遠く、つまり黒にしたいけど正規化のときにdepth大で１に近づいていたから
  imwrite("depth.png", output);
  return output;
}


bool calc(int x,int y,int mode){
  int threshold=20;//しきい値設定
  float z1= (d_img.data[ y * d_img.step + x   ]);//step数　バイト単位
  float z2= (d_img.data[ y * d_img.step + x+1   ]);
  float z3= (d_img.data[ (y+1) * d_img.step + x+1   ]);
  float z4= (d_img.data[ (y+1) * d_img.step + x   ]);
  if(mode==0){
    float z5=max(max(z1,z2),max(z3,z4));
    float z6=min(min(z1,z2),min(z3,z4));
    if(z5-z6>threshold)
      return 0;
  }
  else if(mode==1){
    float z5=max(max(z1,z2),z4);
    float z6=min(min(z1,z2),z4);
    if(z5-z6>threshold)
      return 0;
  }
  else if(mode==2){
    float z5=max(max(z3,z2),z4);
    float z6=min(min(z3,z2),z4);
    if(z5-z6>threshold)
      return 0; 
  }
  return 1;
}
void mycolor(int x,int y){ 
  double value1=(double)img.data[img.channels()*(x+y*img.rows)]/255;//R
  double value2=(double)img.data[img.channels()*(x+y*img.rows)+1]/255;//G
  double value3=(double)img.data[img.channels()*(x+y*img.rows)+2]/255;//B  
  glColor3d(value1,value2,value3);
  return ;
}
void myver(int x,int y){
  glVertex3f((2 *(float)x/d_img.cols-1),(1-2 *(float)y/d_img.rows), (float)(ratio*(maxVal-minVal)*d_img.data[ y * d_img.step + x   ]));
}
int main(int argc, char *argv[])
{
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH );
  glutInitWindowSize(500,500);
  glutCreateWindow(WINDOW_NAME);
  init();
  d_img=Mat::zeros(img.size(),CV_8UC1);
  d_img=dis2dep();
  resize(img,img,d_img.size());
  cvtColor(img,img,CV_BGR2RGB);  
  glutDisplayFunc(glut_display);
  glutKeyboardFunc(glut_keyboard);
  glutMouseFunc(glut_mouse);
  glutMotionFunc(glut_motion);
  glutMainLoop();
  return 0;
}
void init(void){
  glClearColor(0.0, 0.0, 0.0, 1.0);
}
void glut_keyboard(unsigned char key, int x, int y){
  switch(key){
  case 'q':
  case 'Q':
  case '\033':
    exit(0);
    break;
  }
  glutPostRedisplay();
}
void glut_mouse(int button, int state, int x, int y){
  if(button == GLUT_LEFT_BUTTON){
    if(state == GLUT_UP){
      LeftButtonOn = false;
    }else if(state == GLUT_DOWN){
      LeftButtonOn = true;
    }
  }
  if(button == GLUT_RIGHT_BUTTON){
    if(state == GLUT_UP){
      RightButtonOn = false;
    }else if(state == GLUT_DOWN){
      RightButtonOn = true;
    }
  }
}
void glut_motion(int x, int y){
  static  int px = -1, py = -1;
  if(LeftButtonOn == true&&RightButtonOn == true){
    Angle1=0;
    Angle2=0;
    gluLookAt(0,0,0,0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
  }
  else if(LeftButtonOn == true){
    if(px >= 0 && py >= 0){
      Angle1 += (double)-(x - px)/50;
      Angle2 += (double)(y - py)/50;
    }
    px = x;
    py = y;
  }else if(RightButtonOn == true){
    if(px >= 0 && py >= 0){
      Distance += (double)(y - py)/20;
    }
    px = x;
    py = y;
  }else{
    px = -1;
    py = -1;
  }
  glutPostRedisplay();
}
void glut_display(void)
{
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(30.0, 1.0, 0.1, 100);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  gluLookAt(Distance * cos(Angle2) * sin(Angle1), Distance * sin(Angle2),Distance * cos(Angle2) * cos(Angle1),0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glEnable(GL_DEPTH_TEST);
   draw();//点描
  //draw2();//at 四角形
  //draw3();//三角形メッシュ
  //draw4();//ポリゴン　四角形
  //draw5();//立方体 ボクセル
  glFlush();
  glDisable(GL_DEPTH_TEST);
  glutSwapBuffers();
}
void draw(void){
  glPointSize(3);
  glBegin(GL_POINTS);
  for(int y=0;y<d_img.rows;y++){
    for(int x=0;x<d_img.cols;x++){
      mycolor(x,y);
      myver(x,y);
    }
  }
  glEnd();	
}

void draw2(void){
  glBegin(GL_QUADS);
  for(int y=0;y<d_img.rows;y+=1){
    for(int x=0;x<d_img.cols;x+=1){
      int flag=calc(x,y,0);//mode0で四角形
      if(flag){
	mycolor(x,y);
	myver(x,y);
	mycolor(x,y+1);
	myver(x,y+1);
	mycolor(x+1,y+1);
	myver(x+1,y+1);
	mycolor(x+1,y);
	myver(x+1,y);
      }   
    }
  }
  glEnd();	
}

void draw3(void){
  glBegin(GL_TRIANGLES);
  for(int y=0;y<d_img.rows;y+=1){
    for(int x=0;x<d_img.cols;x+=1){
      int flag=calc(x,y,1);//mode1で左上からの三角形
      if(flag){
	mycolor(x,y);
	myver(x,y);
	mycolor(x,y+1);
	myver(x,y+1);
	mycolor(x+1,y);
	myver(x+1,y);
      }
      flag=calc(x,y,2);//mode2で右下からの三角形
      if(flag){
	mycolor(x,y+1);
	myver(x,y+1);
      	mycolor(x+1,y+1);
	myver(x+1,y+1);
	mycolor(x+1,y);
	myver(x+1,y);
      }
      
    }
  }
  glEnd();	
}
 
void draw4(void){
  glBegin(GL_QUADS);
  for(int y=0;y<d_img.rows;y+=1){
    for(int x=0;x<d_img.cols;x+=1){
      int flag=calc(x,y,0);//mode0で四角形
      if(flag){
	mycolor(x,y);
	myver(x,y);
	mycolor(x,y+1);
	myver(x,y+1);
      	mycolor(x+1,y+1);
	myver(x+1,y+1);
	mycolor(x+1,y);
	myver(x+1,y);
      }   
    }
  }
  glEnd();	
}
void draw5(void){//立方体
  for(int y=0;y<d_img.rows;y+=1){
    for(int x=0;x<d_img.cols;x+=1){
      mycolor(x,y);
      glPushMatrix();
      glTranslatef((2 *(float)x/d_img.cols-1),(1-2 *(float)y/d_img.rows), (float)(ratio*(maxVal-minVal)*d_img.data[ y * d_img.step + x   ]));
      // glutSolidCube(0.02);
      glutSolidCube(2.0/d_img.rows);//10ではだめ　イントで入ってるのかな？　概ねあっているがｚ座標がそれよりも大きく変化しているときは穴が開くよね
      glPopMatrix();
    }
  }
  glEnd();	
}
