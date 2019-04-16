#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include<time.h>
using namespace std;
//权值表
int weight[8][8] = { { 500,-25,10,5,5,10,-25,500 },{ -25,-45,1,1,1,1,-45,-25 } ,{ 10,1,3,2,2,3,1,10 },{ 5,1,2,1,1,2,1,5 },{ 5,1,2,1,1,2,1,5 } ,{ 10,1,3,2,2,3,1,10 } ,{ -25,-45,1,1,1,1,-45,-25 } ,{ 500,-25,10,5,5,10,-25,500 } };
struct node {
	char state[9][9];
	vector <node> children;
	int alpha;
	int beta;
	int value;
	int spacenum;//空格数量
	int piecenum;//棋子数量（假设为黑棋）
	int best;
	node* parent;
};

//四个方向的判断
vector <int> judge1(int i, int j, char state[][9], int peopleorcomputer) {
	vector<int> tmpflag;
	for (int k = 0; k < 4; k++) {
		tmpflag.push_back(0);
	}
	int plusi = 0, plusj = 0, minusi = 0, minusj = 0;

	//上
	minusi--;
	if (i + minusi >= 1 && state[i + minusi][j] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i + minusi][j] == '+') {
				while (i + minusi >= 1) {
					minusi--;
					if (state[i + minusi][j] == ' ') break;
					if (state[i + minusi][j] == '+') continue;
					if (state[i + minusi][j] == '*') {
						tmpflag[0] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i + minusi][j] == '*') {
				while (i + minusi >= 1) {
					minusi--;
					if (state[i + minusi][j] == ' ') break;
					if (state[i + minusi][j] == '*') continue;
					if (state[i + minusi][j] == '+') {
						tmpflag[0] = 1;
						break;
					}
				}
			}
		}
	}


	//下
	plusi++;
	if (i + minusi <= 8 && state[i + plusi][j] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i + plusi][j] == '+') {
				while (i + plusi <= 8) {
					plusi++;
					if (state[i + plusi][j] == ' ') break;
					if (state[i + plusi][j] == '+') continue;
					if (state[i + plusi][j] == '*') {
						tmpflag[1] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i + plusi][j] == '*') {
				while (i + plusi <= 8) {
					plusi++;
					if (state[i + plusi][j] == ' ') break;
					if (state[i + plusi][j] == '*') continue;
					if (state[i + plusi][j] == '+') {
						tmpflag[1] = 1;
						break;
					}
				}
			}
		}
	}

	//左
	minusj--;
	if (j + minusj >= 1 && state[i][j + minusj] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i][j + minusj] == '+') {
				while (j + minusj >= 1) {
					minusj--;
					if (state[i][j + minusj] == ' ')break;
					if (state[i][j + minusj] == '+') continue;
					if (state[i][j + minusj] == '*') {
						tmpflag[2] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i][j + minusj] == '*') {
				while (j + minusj >= 1) {
					minusj--;
					if (state[i][j + minusj] == ' ')break;
					if (state[i][j + minusj] == '*') continue;
					if (state[i][j + minusj] == '+') {
						tmpflag[2] = 1;
						break;
					}
				}
			}
		}
	}

	//右
	plusj++;
	if (j + plusj <= 8 && state[i][j + plusj] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i][j + plusj] == '+') {
				while (j + plusj <= 8) {
					plusj++;
					if (state[i][j + plusj] == ' ')break;
					if (state[i][j + plusj] == '+') continue;
					if (state[i][j + plusj] == '*') {
						tmpflag[3] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i][j + plusj] == '*') {
				while (j + plusj <= 8) {
					plusj++;
					if (state[i][j + plusj] == ' ')break;
					if (state[i][j + plusj] == '*') continue;
					if (state[i][j + plusj] == '+') {
						tmpflag[3] = 1;
						break;
					}
				}
			}
		}
	}
	return tmpflag;

}
//对角线四个方向的判断
vector <int> judge2(int i, int j, char state[][9], int peopleorcomputer) {
	vector<int> tmpflag2;
	for (int k = 0; k < 4; k++) {
		tmpflag2.push_back(0);
	}
	int plusi = 0, plusj = 0, minusi = 0, minusj = 0;

	//左上:minusi,minusj
	minusi--;
	minusj--;
	if (i + minusi >= 1 && j + minusj >= 1 && state[i + minusi][j + minusj] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i + minusi][j + minusj] == '+') {
				while (i + minusi >= 1 && j + minusj >= 1) {
					minusi--;
					minusj--;
					if (state[i + minusi][j + minusj] == ' ') break;
					if (state[i + minusi][j + minusj] == '+') continue;
					if (state[i + minusi][j + minusj] == '*') {
						tmpflag2[0] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i + minusi][j + minusj] == '*') {
				while (i + minusi >= 1 && j + minusj >= 1) {
					minusi--;
					minusj--;
					if (state[i + minusi][j + minusj] == ' ') break;
					if (state[i + minusi][j + minusj] == '*') continue;
					if (state[i + minusi][j + minusj] == '+') {
						tmpflag2[0] = 1;
						break;
					}
				}
			}
		}
	}
	minusi = 0;
	minusj = 0;
	//右上：minusi，plusj
	minusi--;
	plusj++;
	if (i + minusi >= 1 && j + plusj <= 8 && state[i + minusi][j + plusj] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i + minusi][j + plusj] == '+') {
				while (i + minusi >= 1 && j + plusj <= 8) {
					minusi--;
					plusj++;
					if (state[i + minusi][j + plusj] == ' ')break;
					if (state[i + minusi][j + plusj] == '+') continue;
					if (state[i + minusi][j + plusj] == '*') {
						tmpflag2[1] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i + minusi][j + plusj] == '*') {
				while (i + minusi >= 1 && j + plusj <= 8) {
					minusi--;
					plusj++;
					if (state[i + minusi][j + plusj] == ' ')break;
					if (state[i + minusi][j + plusj] == '*') continue;
					if (state[i + minusi][j + plusj] == '+') {
						tmpflag2[1] = 1;
						break;
					}
				}
			}
		}
	}
	minusi = 0;
	plusj = 0;
	//右下：plusi,plusj
	plusi++;
	plusj++;
	if (i + plusi <= 8 && j + plusj <= 8 && state[i + plusi][j + plusj] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i + plusi][j + plusj] == '+') {
				while (i + plusi <= 8 && j + plusj <= 8) {
					plusi++;
					plusj++;
					if (state[i + plusi][j + plusj] == ' ')break;
					if (state[i + plusi][j + plusj] == '+') continue;
					if (state[i + plusi][j + plusj] == '*') {
						tmpflag2[2] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i + plusi][j + plusj] == '*') {
				while (i + plusi <= 8 && j + plusj <= 8) {
					plusi++;
					plusj++;
					if (state[i + plusi][j + plusj] == ' ')break;
					if (state[i + plusi][j + plusj] == '*') continue;
					if (state[i + plusi][j + plusj] == '+') {
						tmpflag2[2] = 1;
						break;
					}
				}
			}
		}
	}
	plusi = 0;
	plusj = 0;
	//左下：plusi，minusj
	plusi++;
	minusj--;
	if (i + plusi <= 8 && j + minusj >= 1 && state[i + plusi][j + minusj] != ' ') {
		if (peopleorcomputer == 0) {
			if (state[i + plusi][j + minusj] == '+') {
				while (i + plusi <= 8 && j + minusj >= 1) {
					plusi++;
					minusj--;
					if (state[i + plusi][j + minusj] == ' ')break;
					if (state[i + plusi][j + minusj] == '+') continue;
					if (state[i + plusi][j + minusj] == '*') {
						tmpflag2[3] = 1;
						break;
					}
				}
			}
		}
		else {
			if (state[i + plusi][j + minusj] == '*') {
				while (i + plusi <= 8 && j + minusj >= 1) {
					plusi++;
					minusj--;
					if (state[i + plusi][j + minusj] == ' ')break;
					if (state[i + plusi][j + minusj] == '*') continue;
					if (state[i + plusi][j + minusj] == '+') {
						tmpflag2[3] = 1;
						break;
					}
				}
			}
		}
	}
	return tmpflag2;

}

//寻找到可走位置
vector <string> findthecorrect(char state[][9], int peopleorcomputer) {
	vector <string> position;
	for (int i = 1; i < 9; i++) {
		for (int j = 1; j < 9; j++) {
			if (state[i][j] != ' ')  continue;//该点若是空格才可以下子
			vector <int> flag1, flag2;
			flag1 = judge1(i, j, state, peopleorcomputer);//上下左右判定
			flag2 = judge2(i, j, state, peopleorcomputer);//对角线判定
			int flag11 = 0, flag22 = 0;
			for (int k = 0; k < flag1.size(); ++k)
				if (flag1[k] == 1) {
					flag11 = 1;
					break;
				}
			for (int k = 0; k < flag2.size(); ++k)
				if (flag2[k] == 1) {
					flag22 = 1;
					break;
				}
			if (flag11 == 1 || flag22 == 1) {
				char tmpa = char('0' + i);
				char tmpb = char('0' + j);
				string tmpc = "";
				tmpc += tmpa;
				tmpc += tmpb;
				position.push_back(tmpc);//坐标可行，则添加
			}

		}
	}
	return position;//返回坐标的向量
}



//根据下的位置进行吃子
int capture(char state[][9], int i, int j, int peopleorcomputer) {
	vector <int> flag1, flag2;
	int num = 0;
	flag1 = judge1(i, j, state, peopleorcomputer);//上下左右的可走的点
	flag2 = judge2(i, j, state, peopleorcomputer);//对角线上可以走的点
	int tmpi, tmpj;
	if (peopleorcomputer == 0) {
		for (int k = 0; k < flag1.size(); ++k) {
			if (flag1[k] == 1) {
				switch (k) {
				case 0://上
					tmpi = -1;
					while (state[i + tmpi][j] == '+') {
						state[i + tmpi][j] = '*';
						num++;
						tmpi--;
					}
					break;
				case 1://下
					tmpi = 1;
					while (state[i + tmpi][j] == '+') {
						state[i + tmpi][j] = '*';
						num++;
						tmpi++;
					}
					break;
				case 2://左
					tmpj = -1;
					while (state[i][j + tmpj] == '+') {
						state[i][j + tmpj] = '*';
						num++;
						tmpj--;
					}
					break;
				case 3://右
					tmpj = 1;
					while (state[i][j + tmpj] == '+') {
						state[i][j + tmpj] = '*';
						num++;
						tmpj++;
					}
					break;

				}
			}
		}
		for (int k = 0; k < flag2.size(); k++) {
			if (flag2[k] == 1) {
				switch (k) {
				case 0://左上
					tmpi = -1;
					tmpj = -1;
					while (state[i + tmpi][j + tmpj] == '+') {
						state[i + tmpi][j + tmpj] = '*';
						num++;
						tmpi--;
						tmpj--;
					}
					break;
				case 1://右上
					tmpi = -1;
					tmpj = 1;
					while (state[i + tmpi][j + tmpj] == '+') {
						state[i + tmpi][j + tmpj] = '*';
						num++;
						tmpi--;
						tmpj++;
					}
					break;
				case 2://右下
					tmpi = 1;
					tmpj = 1;
					while (state[i + tmpi][j + tmpj] == '+') {
						state[i + tmpi][j + tmpj] = '*';
						num++;
						tmpi++;
						tmpj++;
					}
					break;
				case 3://左下
					tmpi = 1;
					tmpj = -1;
					while (state[i + tmpi][j + tmpj] == '+') {
						state[i + tmpi][j + tmpj] = '*';
						num++;
						tmpi++;
						tmpj--;
					}
					break;
				}
			}
		}
	}
	else {
		for (int k = 0; k < flag1.size(); ++k) {
			if (flag1[k] == 1) {
				switch (k) {
				case 0://上
					tmpi = -1;
					while (state[i + tmpi][j] == '*') {
						state[i + tmpi][j] = '+';
						num++;
						tmpi--;
					}
					break;
				case 1://下
					tmpi = 1;
					while (state[i + tmpi][j] == '*') {
						state[i + tmpi][j] = '+';
						num++;
						tmpi++;
					}
					break;
				case 2:
					tmpj = -1;
					while (state[i][j + tmpj] == '*') {
						state[i][j + tmpj] = '+';
						num++;
						tmpj--;
					}
					break;
				case 3:
					tmpj = 1;
					while (state[i][j + tmpj] == '*') {
						state[i][j + tmpj] = '+';
						num++;
						tmpj++;
					}
					break;

				}
			}
		}
		for (int k = 0; k < flag2.size(); k++) {
			if (flag2[k] == 1) {
				switch (k) {
				case 0:
					tmpi = -1;
					tmpj = -1;
					while (state[i + tmpi][j + tmpj] == '*') {
						state[i + tmpi][j + tmpj] = '+';
						num++;
						tmpi--;
						tmpj--;
					}
					break;
				case 1:
					tmpi = -1;
					tmpj = 1;
					while (state[i + tmpi][j + tmpj] == '*') {
						state[i + tmpi][j + tmpj] = '+';
						num++;
						tmpi--;
						tmpj++;
					}
					break;
				case 2:
					tmpi = 1;
					tmpj = 1;
					while (state[i + tmpi][j + tmpj] == '*') {
						state[i + tmpi][j + tmpj] = '+';
						num++;
						tmpi++;
						tmpj++;
					}
					break;
				case 3:
					tmpi = 1;
					tmpj = -1;
					while (state[i + tmpi][j + tmpj] == '*') {
						state[i + tmpi][j + tmpj] = '+';
						num++;
						tmpi++;
						tmpj--;
					}
					break;
				}
			}
		}

	}
	return num;
}




//输出当前棋盘局面
void printstate(node node1) {
	cout << "黑棋：*  白棋：+" << endl << endl;
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++)
			cout << node1.state[i][j] << ' ';
		cout << endl;
	}
}

//计算局面评估，权值+行动力加权相加
int calcue(char state[][9], int peopleorcomputer) {
	int result = 0;
	if (peopleorcomputer == 1) {
		for (int i = 1; i < 9; i++) {
			for (int j = 1; j < 9; j++) {
				if (state[i][j] == '+') {
					result += weight[i - 1][j - 1];

				}
			}
		}
		result /= 2;//权值计算
		vector <string> flag1 = findthecorrect(state, 1);
		vector <string> flag2 = findthecorrect(state, 0);
		if (flag1.size() > flag2.size()) result += 50; else result -= 50;//行动力计算

	}
	else {
		for (int i = 1; i < 9; i++) {
			for (int j = 1; j < 9; j++) {
				if (state[i][j] == '*') {
					result += weight[i - 1][j - 1];
				}
			}
		}
		vector <string> flag1 = findthecorrect(state, 0);
		vector <string> flag2 = findthecorrect(state, 1);
		if (flag1.size() > flag2.size()) result += 50; else result -= 50;
	}
	return result;

}

//ai部分，alphabeta剪枝
int ai(node &root, int k, int kmax, int peopleorcomputer) {//建立博弈树
	vector <string> childposition = findthecorrect(root.state, peopleorcomputer);//可以下子的点的坐标向量
	if (childposition.size() == 0 || k > kmax)
		return calcue(root.state, peopleorcomputer);//没有可下的结点再往下发展，则计算当前局面的评估

	if (peopleorcomputer == 1) {//当前结点为max结点
		int maxscore = -10000;
		for (int i = 0; i < childposition.size(); i++) {
			node child;
			for (int k = 0; k < 9; k++) {
				for (int j = 0; j < 9; j++)
					child.state[k][j] = root.state[k][j];
			}
			int tmpi = childposition[i][0] - '0', tmpj = childposition[i][1] - '0';
			child.spacenum = root.spacenum - 1;
			child.alpha = root.alpha;
			child.beta = root.beta;
			child.parent = &root;
			if (peopleorcomputer == 1) {
				child.state[tmpi][tmpj] = '+';
				child.piecenum = root.piecenum - capture(child.state, tmpi, tmpj, peopleorcomputer);
			}
			else {
				child.state[tmpi][tmpj] = '*';
				child.piecenum = root.piecenum + capture(child.state, tmpi, tmpj, peopleorcomputer) + 1;
			}
			root.children.push_back(child);//子节点添加到根节点的孩子中
			int childscore = ai(root.children[i], ++k, kmax, peopleorcomputer ^ 1);//对当前结点进行递归拓展
			if (childscore > maxscore) {//若当前值更大，则更新
				maxscore = childscore;
				root.alpha = maxscore;
				root.best = i;
			}
			if (root.alpha >= root.beta)//若alpha大于等于beta值，break则代表不继续搜索子节点下去
				break;
		}
		return maxscore;
	}
	else {//当前结点为min结点
		int minscore = 10000;
		for (int i = 0; i < childposition.size(); i++) {
			node child;
			for (int k = 0; k < 9; k++) {
				for (int j = 0; j < 9; j++)
					child.state[k][j] = root.state[k][j];
			}
			int tmpi = childposition[i][0] - '0', tmpj = childposition[i][1] - '0';
			child.spacenum = root.spacenum - 1;
			child.alpha = root.alpha;
			child.beta = root.beta;
			child.parent = &root;
			child.state[tmpi][tmpj] = '*';
			child.piecenum = root.piecenum + capture(child.state, tmpi, tmpj, peopleorcomputer) + 1;
			root.children.push_back(child);//子节点添加到根节点的孩子中
			int childscore = ai(root.children[i], ++k, kmax, peopleorcomputer ^ 1);//对当前结点进行递归拓展
			if (childscore < minscore) {//若当前值更小，则更新
				minscore = childscore;
				root.alpha = minscore;
				root.best = i;
			}
			if (root.alpha >= root.beta)//若alpha大于等于beta值，break则代表不继续搜索子节点下去
				break;
		}
		return minscore;
	}

}




//开局，状态初始化
void stateinit(char state[][9]) {
	int tmpcol, tmprow;
	state[0][0] = ' ';
	tmpcol = '1';
	tmprow = 'A';
	for (int i = 1; i < 9; i++) {
		state[0][i] = tmpcol;
		state[i][0] = tmprow;
		tmpcol++;
		tmprow++;
	}
	for (int i = 1; i < 9; i++) {
		for (int j = 1; j < 9; j++) {
			state[i][j] = ' ';
		}
	}
	state[4][4] = '*';//黑棋
	state[5][5] = '*';
	state[5][4] = '+';//白棋
	state[4][5] = '+';
}


int main() {
	node root;
	stateinit(root.state);
	root.piecenum = 2;
	root.spacenum = 60;
	root.alpha = -10000;
	root.beta = 10000;
	char difficult;
	cout << "请选择游戏难度：" << endl << "1   简单虐它" << endl << "2   我得想想怎么虐它" << endl << "3   我可能会被他虐" << endl;
	cin >> difficult;
	while (difficult != '1' && difficult != '2' && difficult != '3') {
		cout << "没这个难度，重选……"<<endl;
		cout << "请选择游戏难度：" << endl << "1   简单虐它" << endl << "2   我得想想怎么虐它" << endl << "3   我可能会被他虐" << endl << endl;
		cin >> difficult;
	}
	while (true) {
		root.parent = NULL;
		vector <string> co;
		co = findthecorrect(root.state, 0);        //轮到人下
		if (co.size() != 0) {   //当前有下子的位置
			for (int k = 0; k < co.size(); k++)
				root.state[co[k][0] - '0'][co[k][1] - '0'] = '.';
			printstate(root);
			cout << "当前比分：" << root.piecenum << ':' << 64 - root.spacenum - root.piecenum << endl;
			cout << endl << "标记.的坐标可以落子，请输入落子的坐标，如‘A2’：";

			string input;
			cin >> input;
			while (input.size() > 2) {
				cout << "请重新输入！坐标间不要有空格及其它无关字符：";
				cin >> input;
			}
			while (input[0]<'A' || input[0]>'H') {
				cout << "请重新输入！坐标是字母在前，数字在后";
				cin >> input;
			}
			int tmpi = input[0] - 'A' + 1, tmpj = input[1] - '0';
			while (root.state[tmpi][tmpj] != '.') {
				cout << "该点不可下！请重新输入：";
				cin >> input;
				tmpi = input[0] - 'A' + 1;
				tmpj = input[1] - '0';
			}

			for (int k = 0; k < co.size(); k++)
				root.state[co[k][0] - '0'][co[k][1] - '0'] = ' ';
			int num = capture(root.state, tmpi, tmpj, 0);             //吃子
			root.state[tmpi][tmpj] = '*';
			root.spacenum--;
			root.piecenum += num + 1;
			cout << "下子结果：" << endl;
			printstate(root);
			cout << "当前比分：" << root.piecenum << ':' << 64 - root.spacenum - root.piecenum << endl;

		}
		else {  //没有下子的位置，电脑继续下子
			printstate(root);
			cout << "当前比分：" << root.piecenum << ':' << 64 - root.spacenum - root.piecenum << endl;
		}
		if (root.spacenum == 0 || (findthecorrect(root.state, 1).size() == 0 && findthecorrect(root.state, 0).size() == 0)) {//黑子下了最后一个子
			int blackpiecenum = root.piecenum, whitepiecenum = 64 - root.piecenum;
			if (blackpiecenum > whitepiecenum) {
				cout << "你赢了！最终比分：" << blackpiecenum << ':' << whitepiecenum << endl;
				system("pause");
				break;
			}
			else if (blackpiecenum == whitepiecenum) {
				cout << "平局！最终比分：" << blackpiecenum << ':' << whitepiecenum << endl;
				system("pause");
				break;
			}
			else {
				cout << "你输了！最终比分：" << blackpiecenum << ':' << whitepiecenum << endl;
				system("pause");
				break;
			}
		}
		if (findthecorrect(root.state, 1).size() != 0) {  //电脑有可以下子的位置
			cout << endl << "电脑正在思考……" << endl;
			double starttime = clock();
			if (difficult == '1') 
				int value = ai(root, 0, 4, 1);     //建树寻找较好的下法并下子
			else if (difficult == '2') 
				int value = ai(root, 0, 5, 1);     //建树寻找较好的下法并下子
			else 
				int value = ai(root, 0, 6, 1);     //建树寻找较好的下法并下子
			
			double endtime = clock();
			cout << endl << "计算用时：" << (endtime - starttime) / 1000 << endl;
			node newnode;
			for (int i = 0; i < 9; i++) {
				for (int j = 0; j < 9; j++)
					newnode.state[i][j] = root.children[root.best].state[i][j];
			}
			newnode.alpha = root.children[root.best].alpha;
			newnode.beta = root.children[root.best].beta;
			newnode.spacenum = root.children[root.best].spacenum;
			newnode.piecenum = root.children[root.best].piecenum;
			root = newnode;  //将当前局面更新为下子之后的局面
			root.children.clear();
		}


	}

}