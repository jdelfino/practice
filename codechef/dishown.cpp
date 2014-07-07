#include <unordered_map>
#include <string>
#include <iostream>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <stdlib.h>

using namespace std;

int heads[10000];
int tails[10000];
int dish_to_chef[10000];
int scores[10000];

#define gc getchar_unlocked
inline int read_int() {
	char c = gc();
	while(c<'0' || c>'9') c = gc();
	int ret = 0;
	while(c>='0' && c<='9') {
		ret = 10 * ret + c - 48;
		c = gc();
	}
	return ret;
}

int main(int argc, char** argv){
	int T = read_int();

	for(int test = 0; test < T; ++test){
		int N = read_int();

		for(int i = 0; i < N; ++i){
			scores[i] = read_int();
			heads[i] = i;
			tails[i] = i;
			dish_to_chef[i] = i;
		}

		int Q = read_int();

		for(int query = 0; query < Q; ++query){
			int tp = read_int();

			if(tp == 0){
				int c1 = dish_to_chef[read_int()-1];
				int c2 = dish_to_chef[read_int()-1];

				if(c1 == c2) {
					fwrite("Invalid query!\n", sizeof(char), 15, stdout);
				} else {

					if(scores[c1] != scores[c2]) {
						int winner = scores[c1] > scores[c2] ? c1 : c2;
						int loser = scores[c1] > scores[c2] ? c2 : c1;

						int d = loser;
						int last = tails[loser];
						while(d != last) {
							dish_to_chef[&heads[d] - heads] = winner;
							d = heads[d];
						}
						dish_to_chef[&heads[last] - heads] = winner;
						heads[tails[winner]] = loser;
						tails[winner] = tails[loser];
					}
				}

			} else {
				int answ = dish_to_chef[read_int()-1] + 1;

				int p = pow(10, (int)log10(answ));
				while(p > 0){
					putc_unlocked('0' + (answ / p), stdout);
					answ %= p;
					p /= 10;
				}
				putc_unlocked('\n', stdout);
			}
		}
	}

}
