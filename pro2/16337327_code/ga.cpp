#include <iostream>
#include <time.h>
#include <vector>
#include <algorithm>
using namespace std;
vector <double> bestweight;//���Ȩ��
char board2[8][8];
struct Node {
	int mode;
	char board[8][8];
	double score;
	pair<int, int> action;
	vector<Node> children;
	Node(char raw_board[8][8], int cur_mode) {
		mode = cur_mode;
		for (int i = 0; i < 8; i++)
			for (int j = 0; j < 8; j++)
				board[i][j] = raw_board[i][j];
	}
};

struct weightstruct {
	vector<double> subweight;
	int adapt;
};

class Othello {
private:
	int square_weights[8][8] = {
		{400, -30, 11, 8, 8, 11, -30, 400},
		{-30, -70, -4, 1, 1, -4, -70, -30},
		{11, -4, 2, 2, 2, 2, -4, 11},
		{8, 1, 2, -3, -3, 2, 1, 8},
		{8, 1, 2, -3, -3, 2, 1, 8},
		{11, -4, 2, 2, 2, 2, -4, 11},
		{-30, -70, -4, 1, 1, -4, -70, -30},
		{400, -30, 11, 8, 8, 11, -30, 400},
	};
	int direction[8][2] = { {0, 1}, {0, -1}, {1, 1}, {1, 0}, {1, -1}, {-1, 0}, {-1, 1}, {-1, -1} };
	int limit;

public:
	Othello(int depth) { limit = depth; }

	void init_board(char board[8][8]) {
		for (int i = 0; i < 8; ++i)
			memset(board[i], ' ', 8);
		board[3][4] = board[4][3] = '@';
		board[3][3] = board[4][4] = 'O';
	}

	void print_board(char board[8][8], vector<pair<int, int>> next_step) {
		// ��ӡ���̣�����board�����̣�next_step��������λ��
		char col = 'A';
		cout << endl << ' ';
		for (char i = 0; i < 8; i++)
			cout << ' ' << char(col + i);
		cout << endl;
		for (int i = 0; i < 8; i++) {
			cout << i + 1 << ' ';
			for (int j = 0; j < 8; ++j)
				if (find(next_step.begin(), next_step.end(), make_pair(i, j)) == next_step.end())
					cout << board[i][j] << ' ';
				else
					cout << "* ";
			cout << endl;
		}
		auto nums = count_number(board);
		cout << "����:���� = " << nums.first << ':' << nums.second << endl;
	}

	bool is_on_board(int row, int col) {
		// �ж��Ƿ���������
		return row < 8 && row >= 0 && col < 8 && col >= 0;
	}

	vector<pair<int, int>> show_places(char board[8][8], char turn) {
		// Ѱ�ҿ�����λ�ã�����board�����̣�turn���������ӻ��������
		vector<pair<int, int>> next_step;
		char item = turn == '@' ? '@' : 'O', opp = turn == '@' ? 'O' : '@';
		for (int i = 0; i < 8; ++i)
			for (int j = 0; j < 8; ++j)
				if (board[i][j] == ' ' && !flip_dirs(board, make_pair(i, j), item).empty())
					next_step.push_back(make_pair(i, j));
		return next_step;
	}

	vector<int> flip_dirs(char board[8][8], pair<int, int> pos, char color) {
		// �жϷ�ת����
		int x = pos.first, y = pos.second;
		vector<int> dirs;
		char opp = color == '@' ? 'O' : '@';
		for (int i = 0; i < 8; ++i) {
			x += direction[i][0];
			y += direction[i][1];
			if (is_on_board(x, y) && board[x][y] == opp) {
				while (is_on_board(x, y) && board[x][y] == opp) {
					x += direction[i][0];
					y += direction[i][1];
				}
				if (is_on_board(x, y) && board[x][y] == color) dirs.push_back(i);
			}
			x = pos.first;
			y = pos.second;
		}
		return dirs;
	}

	void flip(char board[8][8], pair<int, int> action, char color) {
		// ִ�з�ת����
		vector<int> dirs = flip_dirs(board, action, color);
		char opp = color == '@' ? 'O' : '@';
		int x = action.first, y = action.second;
		for (int i = 0; i < dirs.size(); ++i) {
			x += direction[dirs[i]][0];
			y += direction[dirs[i]][1];
			while (is_on_board(x, y) && board[x][y] == opp) {
				board[x][y] = color;
				x += direction[dirs[i]][0];
				y += direction[dirs[i]][1];
			}
			x = action.first;
			y = action.second;
		}
	}

	bool is_over(char board[8][8]) {
		// �жϱ����Ƿ����
		auto list1 = show_places(board, '@');
		auto list2 = show_places(board, 'O');
		return list1.empty() && list2.empty();
	}

	void player_play(char board[8][8], vector<pair<int, int>> next_step, char turn) {
		cout << "���������꣨���磺A1����";
		while (true) {
			char col, row;
			cin >> col >> row;
			if (col >= 'A' && col <= 'H' && row >= '1' && row <= '8') {
				auto action = make_pair(row - '1', col - 'A');
				if (find(next_step.begin(), next_step.end(), action) != next_step.end()) {
					move(board, action, turn);
					break;
				}
			}
			cout << "��Чλ��,���������루���磺A1����";
		}
		cout << endl;
	}

	bool is_stable(char board[8][8], int x, int y) {
		for (int i = 0; i < 8; ++i)
			for (int nx = x + direction[i][0], ny = y + direction[i][1]; is_on_board(nx, ny); nx += direction[i][0], ny += direction[i][1])
				if (board[nx][ny] == ' ')
					return false;
		return true;
	}

	weightstruct ga(double result1, double result2, double result3, double result4, double result5, double result6, double result7) {
		vector<weightstruct> randweight;
		//�������10��Ȩ������
		srand(time(0));
		
		for (int i = 0; i < 10; ++i) {
			vector<double> weighti;
			weightstruct tmp;
			double sum = 0;
			for (int k = 0; k < 7; k++) {
				double tmp = rand() / double(RAND_MAX);
				weighti.push_back(tmp);
				sum += tmp;
			}
			for (int k = 0; k < 7; k++) {
				weighti[k] /= sum;
				tmp.subweight.push_back(weighti[k]);
			}
			tmp.adapt = 0;
			randweight.push_back(tmp);
		}
		weightstruct runner = randweight[0];
		int n = 10;//����30����������
		while (n--) {
			//�Ե�ǰ10����������PK
			double res1, res2;
			for (int i = 0; i < 10; i++) {
				for (int j = i + 1; j < 10; j++) {
					res1 = randweight[i].subweight[0] * result1 + randweight[i].subweight[1] * result2 + randweight[i].subweight[2] * result3 + randweight[i].subweight[3] * result4 + randweight[i].subweight[4] * result5 + randweight[i].subweight[5] * result6 + randweight[i].subweight[6] * result7;
					res2 = randweight[j].subweight[0] * result1 + randweight[j].subweight[1] * result2 + randweight[j].subweight[2] * result3 + randweight[j].subweight[3] * result4 + randweight[j].subweight[4] * result5 + randweight[j].subweight[5] * result6 + randweight[j].subweight[6] * result7;
					if (res1 > res2) randweight[i].adapt += 1;  else randweight[j].adapt += 1;

				}
			}
			//����Ա���ܣ����и��ӵ���̭
			for (int j = 0; j < 10; ++j) {
				res1 = runner.subweight[0] * result1 + runner.subweight[1] * result2 + runner.subweight[2] * result3 + runner.subweight[3] * result4 + runner.subweight[4] * result5 + runner.subweight[5] * result6 + runner.subweight[6] * result7;
				res2 = randweight[j].subweight[0] * result1 + randweight[j].subweight[1] * result2 + randweight[j].subweight[2] * result3 + randweight[j].subweight[3] * result4 + randweight[j].subweight[4] * result5 + randweight[j].subweight[5] * result6 + randweight[j].subweight[6] * result7;
				if (res1 > res2) randweight[j].adapt -=2;
			}
			//��̭�����
			weightstruct tmp2;
			for (int i = 0; i < 10; i++) {
				for (int j = 0; j < 9 - i; j++) {
					if (randweight[j].adapt < randweight[j + 1].adapt) {
						tmp2 = randweight[j];
						randweight[j] = randweight[j + 1];
						randweight[j + 1] = tmp2;
					}
				}
			}
			runner = randweight[0];//����Ա����������
			if (n == 1) break;
			vector<weightstruct> newrandweight;
			//���Ʋ��֣��˴�ѡ����Ӧ����ߵ�3�����и��ƣ�����Ҫ���ϸ��ʣ��˴�����Ϊ90%���ơ�
			int pro = rand() % 10;
			if (pro != 9) {
				newrandweight.push_back(randweight[0]);
				newrandweight.back().adapt = 0;
				newrandweight.push_back(randweight[1]);
				newrandweight.back().adapt = 0;
				newrandweight.push_back(randweight[2]);
				newrandweight.back().adapt = 0;
			}
			else {
				for (int j = 0; j < 3; j++) {
					vector<double> weighti;
					weightstruct tmp;
					double sum = 0;
					for (int k = 0; k < 7; k++) {
						double tmp = rand() / double(RAND_MAX);
						weighti.push_back(tmp);
						sum += tmp;
					}
					for (int k = 0; k < 7; k++) {
						weighti[k] /= sum;
						tmp.subweight.push_back(weighti[k]);
					}
					tmp.adapt = 0;
					newrandweight.push_back(tmp);
				}
				
			}
			//���沿�֣�ģ����ֳ����12��13��14��23��24��34���н���
			for (int i = 0; i < 4; i++) {
				for (int j = i + 1; j < 4; j++) {
					weightstruct tmp;
					tmp.adapt = 0;
					double tmpsum = 0;
					int rand2 = rand() % 2;
					int cut = rand() % 7;
					for (int k = 0; k < 7; k++) {					
						if (rand2 == 0) {
							if (k <= cut) {
								tmp.subweight.push_back(randweight[i].subweight[k]);
								tmpsum += randweight[i].subweight[k];
							}
							else {
								tmp.subweight.push_back(randweight[j].subweight[k]);
								tmpsum += randweight[j].subweight[k];
							}
						}

						else {
							if (k <= cut) {
								tmp.subweight.push_back(randweight[j].subweight[k]);
								tmpsum += randweight[j].subweight[k];
							}
							else {
								tmp.subweight.push_back(randweight[i].subweight[k]);
								tmpsum += randweight[i].subweight[k];
							}
							
						}
					}
					for (int k = 0; k < 7; k++) {
						tmp.subweight[k] = tmp.subweight[k] / tmpsum;
					}
					newrandweight.push_back(tmp);

				}
			}
			weightstruct tmp3 = randweight[0];
			tmp3.adapt = 0;
			//���첿�֣����ѡ��һ������Ԫ�ظ����µ����ֵ
			double replace = (rand() / double(RAND_MAX));
			double sum = 0;
			int rand3 = rand() % 7;
			for (int k = 0; k < 7; k++) {
				if (k == rand3)
					sum += replace;
				else
					sum += tmp3.subweight[k];

			}
			for (int k = 0; k < 7; k++) {
				if (k == rand3) {
					tmp3.subweight[k] = replace / sum;
					continue;
				}
				else {
					tmp3.subweight[k] = tmp3.subweight[k] / sum;
				}
			}
			newrandweight.push_back(tmp3);
			randweight = newrandweight;
		}
		return randweight[0];

	}


	weightstruct evaluate2(char color) {
		
		int sideVal[8] = { 1, 2, 3, 4, 5, 6, 7, 8 };
		int corner_pos[4][2] = { { 0, 0 },{ 0, 7 },{ 7, 0 },{ 7, 7 } };
		int mystonecount = 0, opstonecount = 0, mystable = 0, oppstable = 0;
		double score = 0, rateeval = 0, moveeval = 0, sidestableeval = 0, cornereval = 0, stableeval = 0, neareval = 0;
		char opp = color == '@' ? 'O' : '@';

		//����λ����������ֵ
		for (int i = 0; i < 8; ++i)
			for (int j = 0; j < 8; ++j)
				if (board2[i][j] == color) {
					score += square_weights[i][j];
					mystonecount++;
				}
				else if (board2[i][j] == opp) {
					score -= square_weights[i][j];
					opstonecount++;
				}

				//����ڰ��ӱ�������ֵ
				if (mystonecount > opstonecount)
					rateeval = 100.0 * mystonecount / (mystonecount + opstonecount);
				else if (mystonecount < opstonecount)
					rateeval = -100.0 * opstonecount / (mystonecount + opstonecount);
				else
					rateeval = 0;

				//�����ǵĹ���ֵ
				int mynear = 0, oppnear = 0;
				for (int i = 0; i < 4; ++i) {
					int x = corner_pos[i][0], y = corner_pos[i][1];
					if (board2[x][y] == ' ')
						for (int j = 0; j < 8; ++j) {
							int nx = x + direction[j][0], ny = y + direction[j][1];
							if (is_on_board(nx, ny))
								if (board2[nx][ny] == color)
									mynear++;
								else if (board2[nx][ny] == opp)
									oppnear++;
						}
				}
				neareval = -24.5 * (mynear - oppnear);


				//�����ж�������ֵ
				int mymove = show_places(board2, color).size();
				int opmove = show_places(board2, opp).size();
				//����ҷ�û�еط����ӣ���ô�趨�ص͵��ж�������ֵ
				if (mymove == 0)
					moveeval = -450;
				//����Է�û�еط����ӣ���ô�趨�ظߵ��ж�������ֵ
				else if (opmove == 0)
					moveeval = 150;
				else if (mymove > opmove)
					moveeval = (100.0 * mymove) / (mymove + opmove);
				else if (mymove < opmove)
					moveeval = -(100.0 * opmove) / (mymove + opmove);
				else
					moveeval = 0;

				//�����ڲ��ȶ��ӹ���ֵ
				for (int i = 0; i < 8; ++i)
					for (int j = 0; j < 8; ++j)
						if (board2[i][j] != ' ' && is_stable(board2, i, j))
							if (board2[i][j] == color)
								mystable++;
							else
								oppstable++;
				stableeval = 12.5 * (mystable - oppstable);

				//����߽��ȶ������ֵ
				int myside = 0, opside = 0, myconer = 0, opconer = 0;
				for (int i = 0; i < 4; ++i)
					if (board2[corner_pos[i][0]][corner_pos[i][1]] == color) {
						myconer++;
						for (int j = 0; j < 8; ++j)
							if (board2[corner_pos[i][0]][j] == color)
								myside += sideVal[j];
							else
								break;
						for (int j = 0; j < 8; ++j)
							if (board2[j][corner_pos[i][1]] == color)
								myside += sideVal[j];
							else
								break;
					}
					else if (board2[corner_pos[i][0]][corner_pos[i][1]] == opp) {
						opconer++;
						for (int j = 0; j < 8; ++j)
							if (board2[corner_pos[i][0]][j] == opp)
								opside += sideVal[j];
							else
								break;
						for (int j = 0; j < 8; ++j)
							if (board2[j][corner_pos[i][1]] == opp)
								opside += sideVal[j];
							else
								break;
					}
					sidestableeval = 2.5 * (myside - opside);
					cornereval = 25 * (myconer - opconer);

					//����������ֹ���ֵ
					return ga(score, moveeval, sidestableeval, cornereval, rateeval, stableeval, neareval);

	}



	double evaluate(char board[8][8], char color) {
		int sideVal[8] = { 1, 2, 3, 4, 5, 6, 7, 8 };
		int corner_pos[4][2] = { {0, 0}, {0, 7}, {7, 0}, {7, 7} };
		int mystonecount = 0, opstonecount = 0, mystable = 0, oppstable = 0;
		double score = 0, rateeval = 0, moveeval = 0, sidestableeval = 0, cornereval = 0, stableeval = 0, neareval = 0;
		char opp = color == '@' ? 'O' : '@';

		//����λ����������ֵ
		for (int i = 0; i < 8; ++i)
			for (int j = 0; j < 8; ++j)
				if (board[i][j] == color) {
					score += square_weights[i][j];
					mystonecount++;
				}
				else if (board[i][j] == opp) {
					score -= square_weights[i][j];
					opstonecount++;
				}

				//����ڰ��ӱ�������ֵ
				if (mystonecount > opstonecount)
					rateeval = 100.0 * mystonecount / (mystonecount + opstonecount);
				else if (mystonecount < opstonecount)
					rateeval = -100.0 * opstonecount / (mystonecount + opstonecount);
				else
					rateeval = 0;

				//�����ǵĹ���ֵ
				int mynear = 0, oppnear = 0;
				for (int i = 0; i < 4; ++i) {
					int x = corner_pos[i][0], y = corner_pos[i][1];
					if (board[x][y] == ' ')
						for (int j = 0; j < 8; ++j) {
							int nx = x + direction[j][0], ny = y + direction[j][1];
							if (is_on_board(nx, ny))
								if (board[nx][ny] == color)
									mynear++;
								else if (board[nx][ny] == opp)
									oppnear++;
						}
				}
				neareval = -24.5 * (mynear - oppnear);


				//�����ж�������ֵ
				int mymove = show_places(board, color).size();
				int opmove = show_places(board, opp).size();
				//����ҷ�û�еط����ӣ���ô�趨�ص͵��ж�������ֵ
				if (mymove == 0)
					moveeval = -450;
				//����Է�û�еط����ӣ���ô�趨�ظߵ��ж�������ֵ
				else if (opmove == 0)
					moveeval = 150;
				else if (mymove > opmove)
					moveeval = (100.0 * mymove) / (mymove + opmove);
				else if (mymove < opmove)
					moveeval = -(100.0 * opmove) / (mymove + opmove);
				else
					moveeval = 0;

				//�����ڲ��ȶ��ӹ���ֵ
				for (int i = 0; i < 8; ++i)
					for (int j = 0; j < 8; ++j)
						if (board[i][j] != ' ' && is_stable(board, i, j))
							if (board[i][j] == color)
								mystable++;
							else
								oppstable++;
				stableeval = 12.5 * (mystable - oppstable);

				//����߽��ȶ������ֵ
				int myside = 0, opside = 0, myconer = 0, opconer = 0;
				for (int i = 0; i < 4; ++i)
					if (board[corner_pos[i][0]][corner_pos[i][1]] == color) {
						myconer++;
						for (int j = 0; j < 8; ++j)
							if (board[corner_pos[i][0]][j] == color)
								myside += sideVal[j];
							else
								break;
						for (int j = 0; j < 8; ++j)
							if (board[j][corner_pos[i][1]] == color)
								myside += sideVal[j];
							else
								break;
					}
					else if (board[corner_pos[i][0]][corner_pos[i][1]] == opp) {
						opconer++;
						for (int j = 0; j < 8; ++j)
							if (board[corner_pos[i][0]][j] == opp)
								opside += sideVal[j];
							else
								break;
						for (int j = 0; j < 8; ++j)
							if (board[j][corner_pos[i][1]] == opp)
								opside += sideVal[j];
							else
								break;
					}
					sidestableeval = 2.5 * (myside - opside);
					cornereval = 25 * (myconer - opconer);

					//����������ֹ���ֵ
					return score * bestweight[0] + moveeval * bestweight[1] + sidestableeval * bestweight[2] + cornereval * bestweight[3] + rateeval * bestweight[4] + stableeval * bestweight[5] + neareval * bestweight[6];
	}

	void move(char board[8][8], pair<int, int> action, char color) {
		board[action.first][action.second] = color;
		flip(board, action, color);
	}

	pair<int, int> count_number(char board[8][8]) {
		int b_num = 0, w_num = 0;
		for (int i = 0; i < 8; ++i)
			for (int j = 0; j < 8; ++j)
				if (board[i][j] == '@')
					b_num++;
				else if (board[i][j] == 'O')
					w_num++;
		return make_pair(b_num, w_num);
	}

	void random_play(char board[8][8], char color) {
		auto places = show_places(board, color);
		int index = rand() % places.size();
		move(board, places[index], color);
	}

	void ai_play(char board[8][8], char color, int depth) {
		char opp = color == '@' ? 'O' : '@';
		Node root = Node(board, 2);
		cout << "\nIDIOT����˼��...\n";
		double starttime = clock();
		int index = alphabetapruning(root, color, opp, 1, depth, -100000.0, 100000.0);
		cout << "IDIOT������λ��Ϊ��" << char(root.children[index].action.second + 'A') << root.children[index].action.first + 1 << endl;
		double endtime = clock();
		cout << "IDIOT˼����ʱ��" << (endtime - starttime) / 1000 << 's' << endl;
		move(board, root.children[index].action, color);
		root.children.clear();
		cout << endl;
	}

	double alphabetapruning(Node &root, char ai, char player, int mode, int depth, double alpha, double beta) {
		//mode=0ʱ��ʾMAX��ڵ㣬mode=1ʱ��ʾMIN��ڵ�
		char color = mode == 1 ? ai : player, opp = color == '@' ? 'O' : '@';
		auto avaiplaces = show_places(root.board, color);	//�õ������ӵ�λ��
		double v;
		if (depth == limit) {
			for (int i = 0; i < avaiplaces.size(); ++i) {
				Node newnode = Node(root.board, mode);		//�½��ӽڵ�
				newnode.action = avaiplaces[i];				//��¼�ýڵ����ӵ�λ��
				move(newnode.board, avaiplaces[i], color);	//���Ӻ����̷����仯
				int oppmode = mode == 1 ? 0 : 1;			//������һ��mode
				auto places = show_places(newnode.board, opp);	//�õ��Է������ӵ�λ��
				if (places.size() != 0)
					//����Է����п����ӵ�λ�ã���ݹ�����
					newnode.score = alphabetapruning(newnode, ai, player, oppmode, depth - 1, alpha, beta);
				else
					//����Է�û�еط����ӣ���������ǰ���
					newnode.score = evaluate(newnode.board, color);
				root.children.push_back(newnode);			//�����µ��ӽڵ�
			}
			int index;
			double max = -100000.0;
			//�õ�����ֵ��ߵ��߷�
			for (int i = 0; i < root.children.size(); ++i)
				if (root.children[i].score > max) {
					index = i;
					max = root.children[i].score;
				}
			cout << "IDIOT���߷�����Ӧ�Ĺ���ֵ��";
			for (int i = 0; i < root.children.size(); ++i) {
				cout << char(root.children[i].action.second + 'A') << root.children[i].action.first + 1 << ':' << root.children[i].score << "  ";
			}
			cout << endl;
			//���ع���ֵ��ߵ��߷�
			return index;
		}
		if (mode == 0) {
			//MAX��ڵ�
			v = -100000.0;
			for (int i = 0; i < avaiplaces.size(); ++i) {
				Node newnode = Node(root.board, mode);		//�½��ӽڵ�
				newnode.action = avaiplaces[i];				//��¼�ýڵ����ӵ�λ��
				move(newnode.board, avaiplaces[i], color);	//���Ӻ����̷����仯
				int oppmode = mode == 1 ? 0 : 1;			//������һ��mode
				auto places = show_places(newnode.board, opp);	//�õ��Է������ӵ�λ��
				if (depth != 1 && places.size() != 0) {
					//δ������������ҶԷ��еط����ӣ���ݹ�����������v��alphaֵ
					v = max(v, alphabetapruning(newnode, ai, player, oppmode, depth - 1, alpha, beta));
					alpha = max(alpha, v);
					if (beta <= alpha)	//alpha��֦
						break;
				}
				else {
					//����������ƻ�Է����ӿ��£���������ǰ��ֲ�����vֵ
					newnode.score = evaluate(newnode.board, ai);
					v = max(v, newnode.score);
				}
			}
		}
		else {
			//MIN��ڵ�
			v = 100000.0;
			for (int i = 0; i < avaiplaces.size(); ++i) {
				Node newnode = Node(root.board, mode);		//�½��ӽڵ�
				newnode.action = avaiplaces[i];;			//��¼�ýڵ����ӵ�λ��
				move(newnode.board, avaiplaces[i], color);	//���Ӻ����̷����仯
				int oppmode = mode == 1 ? 0 : 1;			//������һ��mode
				auto places = show_places(newnode.board, opp);	//�õ��Է������ӵ�λ��
				if (depth != 1 && places.size() != 0) {
					//δ������������ҶԷ��еط����ӣ���ݹ�����������v��betaֵ
					v = min(v, alphabetapruning(newnode, ai, player, oppmode, depth - 1, alpha, beta));
					beta = min(beta, v);
					if (beta <= alpha)	//beta��֦
						break;
				}
				else {
					//����������ƻ�Է����ӿ��£���������ǰ��ֲ�����vֵ
					newnode.score = evaluate(newnode.board, ai);
					v = min(v, newnode.score);
				}
			}
		}
		//����ʱ���ռ�õ��ڴ�
		root.children.clear();
		return v;
	}
	weightstruct ave(weightstruct weightmp1, weightstruct weightmp2) {
		weightstruct returnweight;
		double sum = 0;
		for (int i = 0; i < weightmp1.subweight.size(); ++i) {
			sum += (weightmp1.subweight[i] + weightmp2.subweight[i]) / 2;
			returnweight.subweight.push_back((weightmp1.subweight[i] + weightmp2.subweight[i]) / 2);
		}
		for (int i = 0; i < returnweight.subweight.size(); ++i) {
			returnweight.subweight[i] /= sum;
		}
		return returnweight;
	}
	vector <double> ave2(vector <weightstruct> weights) {
		for (int i = 0; i < weights.size(); ++i) {
			for (int j = 0; j < 7; ++j)
				cout << weights[i].subweight[j] << ' ';
			cout << endl;
		}
		vector <double> bestweight;
		//��ֵ
		for (int i = 0; i < 7; i++) {
			bestweight.push_back(0);
			for (int j = 0; j < weights.size(); ++j) {
				bestweight[i] += weights[j].subweight[i];
			}
			bestweight[i] /= weights.size();
		}
		//��һ��
		double sum = 0;
		for (int i = 0; i < 7; ++i) 
			sum += bestweight[i];
		for (int i = 0; i < 7; ++i)
			bestweight[i] /= sum;
		return bestweight;

		
	}

	int game_run() {
		cout << "��ѡ��1Ϊ���壬2Ϊ���壩��";
		int choose = 1;
		cin>>choose;
		char player = choose == 1 ? '@' : 'O', ai = choose == 1 ? 'O' : '@';
		cout << "\n��Ϸ��ʼ��\n@Ϊ���壬OΪ����,*Ϊ������λ��\n\n";
		char current_turn = '@';
		char board[8][8];
		int n = 60;
		vector<pair<int, int>> next_step;
		init_board(board);
		vector<weightstruct> weights;
		weightstruct weightmp;
		int outn = 500;
		cout << "��ʼ���С������Եȡ���"<< endl;
		while (outn--) {
			n = 60;
			while (n--) {
				for (int i = 0; i < 8; i++) {
					for (int j = 0; j < 8; j++)
						board2[i][j] = board[i][j];
				}
				if (n % 2 == 0)
					weights.push_back(ave(evaluate2(current_turn), weightmp));
				else
					weightmp = evaluate2(current_turn);



				next_step = show_places(board, current_turn);
				if (next_step.empty()) {
					current_turn = current_turn == '@' ? 'O' : '@';
					next_step.clear();
					continue;
				}
				if (current_turn == player) {
					random_play(board, player);
				}
				else {
					random_play(board, ai);
				}
				next_step.clear();

				current_turn = current_turn == '@' ? 'O' : '@';


			}
			init_board(board);
			next_step.clear();
		}
		bestweight = ave2(weights);
		init_board(board);
		next_step.clear();
		limit = 4;

		while (!is_over(board)) {
			next_step = show_places(board, current_turn);
			if (next_step.empty()) {
				current_turn = current_turn == '@' ? 'O' : '@';
				next_step.clear();
				continue;
			}
			if (current_turn == player) {
				print_board(board, next_step);
				cout << "\n�ֵ���ң�";
				//player_play(board, next_step, current_turn);
				random_play(board, player);
			}
			else {
				print_board(board, next_step);
				ai_play(board, ai, limit);
			}
			next_step.clear();
			current_turn = current_turn == '@' ? 'O' : '@';
		}
		auto nums = count_number(board);
		print_board(board, next_step);
		cout << "��Ϸ������" << endl;
		if (nums.first > nums.second) {
			cout << "����ʤ����" << endl;
			return 0;
		}
		else if (nums.first < nums.second) {
			cout << "����ʤ����" << endl;
			return 1;
		}
		else {
			cout << "ƽ�֣�" << endl;
			return 0;
		}
	}
};


int main() {
	auto tmp = Othello(3);
	int tmp2 = 500;
	tmp.game_run();
	system("pause");
	return 0;
}