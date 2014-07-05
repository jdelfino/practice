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
typedef tuple<int,int,int> Test;

struct Chef {
	int id;
	vector<int> dishes;
	int score;

	inline Chef(int id_, const vector<int> &dishes_, int score_) :
	id(id_), dishes(dishes_), score(score_) 
	{}

	Chef(): Chef(-1, vector<int>(), -1) {}
};

std::ostream& operator<<(std::ostream &strm, const Chef &chef) {
	strm << "Chef(id: " << chef.id << ", score: " << chef.score << ", dishes: [";
	for(auto dish : chef.dishes) {
		strm << dish << ", ";
	}
	strm << "])";
	return strm;
}

inline void output(const std::string &val){
	fwrite(val.c_str(), sizeof(char), val.size(), stdout);
}

vector<Chef> *chefs;
unordered_map<int, Chef*> *dish_to_chef;

float total_init = 0.0;
float total_comp = 0.0;
float total_insert = 0.0;
float total_lookup = 0.0;

void do_test(const vector<int> &scores, const vector<Test> &queries){
	//clock_t io_start = clock();
	//stringstream answers;

	for(int i = 0; i < scores.size(); ++i){
		Chef &c = (*chefs)[i];
		c.id = i;
		c.dishes.clear();
		c.dishes.push_back(i);
		c.score = scores[i];
		(*dish_to_chef)[i] = &c;

	}

	//total_init += (clock() - io_start) / (double) CLOCKS_PER_SEC;

	//clock_t comp_start = clock();
	for(const auto &query : queries){
		//cout << "(" << get<0>(query) << ", " << get<1>(query) << ", " << get<2>(query) << ")" << endl;

		if(get<0>(query) == 0){
			//clock_t lstart = clock();
			auto dtc1 = dish_to_chef->find(get<1>(query));
			Chef *c1 = dtc1->second;

			auto dtc2 = dish_to_chef->find(get<2>(query));
			Chef *c2 = dtc2->second;

			if(c1 == c2) {
				fwrite("Invalid query!\n", sizeof(char), 15, stdout);
				//output("Invalid query!\n");
			} else {

				//cout << c1->id << " vs " << c2->id << endl;
				if(c1->score != c2->score) {
					Chef *winner;
					Chef *loser;
					if(c1->score > c2->score){
						winner = c1;
						loser = c2;
						dtc2->second = c1;
					} else {
						winner = c2;
						loser = c1;
						dtc1->second = c2;
					}
					//cout << "winner: " << winner->id << " loser: " << loser->id << endl;
					//clock_t ins_start = clock();

					for(int od : loser->dishes){
						if(od == dtc1->first || od == dtc2->first) continue;
						(*dish_to_chef)[od] = winner;
					}

					//winner->dishes.reserve(winner->dishes.size() + loser->dishes.size());
					winner->dishes.insert(
						winner->dishes.end(), 
						loser->dishes.begin(), 
						loser->dishes.end());
					//total_insert += (clock() - ins_start) / (double) CLOCKS_PER_SEC;
					//loser->dishes = vector<int>();
				}
			}
			//total_lookup += (clock() - lstart) / (double) CLOCKS_PER_SEC;

		} else {
			//clock_t ins_start = clock();

			int answ = (*dish_to_chef)[get<1>(query)]->id + 1;
			//answers << answ << "\n";
			/*
			char cansw[6];
			itoa(answ, answ, 10);
			for(char c : cansw){
				putc_unlocked(c, stdout);
				if(c == '\n'){
					break;
				}
			}
			*/

 			/*
 			char cansw[7];
			sprintf(cansw, "%d\n", answ);
			output(cansw);
			*/

 			//printf("%d\n", answ);
 			
 			int p = pow(10, (int)log10(answ));
 			//cout << answ << " " << p << endl;
 			while(p > 0){
 				putc_unlocked('0' + (answ / p), stdout);
				answ %= p;
				p /= 10;
			}
			putc_unlocked('\n', stdout);
			
			/*
 			char cansw[7];
			sprintf(cansw, "%d\n", answ);
 			for(auto c : cansw){
				putc_unlocked(c, stdout);
				if(c == '\n'){
					break;
				}
 			}
 			*/

 			//cout << dish_to_chef[get<1>(query)]->id + 1 << endl;
			/*
			for(auto c : dish_to_chef){
				cout << c.first << "->" << c.second->id << endl;
			}
			*/
			//total_insert += (clock() - ins_start) / (double) CLOCKS_PER_SEC;

		}
	}
	//total_comp += (clock() - comp_start) / (double) CLOCKS_PER_SEC;
	//output(answers.str());
}

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
	//cin.sync_with_stdio(false);

	//clock_t start = clock();
	//float total_io = 0.0;
	//float total_do = 0.0;

	int T = read_int();

	chefs = new vector<Chef>(10000);
	dish_to_chef = new unordered_map<int, Chef*>(10000);

	for(int test = 0; test < T; ++test){
		int N = read_int();

		//clock_t io_start = clock();

		vector<int> scores;
		scores.reserve(N);
		for(int i = 0; i < N; ++i){
			scores.push_back(read_int());
		}

		int Q = read_int();

		vector<Test> *queries = new vector<Test>;
		queries->reserve(Q);

		for(int query = 0; query < Q; ++query){
			int tp = read_int();

			if(tp == 0){
				queries->push_back(make_tuple(0, read_int()-1, read_int()-1));
			} else {
				queries->push_back(make_tuple(1, read_int()-1, -1));
			}
		}
		
		//total_io += (clock() - io_start) / (double) CLOCKS_PER_SEC;

		//clock_t do_start = clock();
		do_test(scores, *queries);
		//total_do += (clock() - do_start) / (double) CLOCKS_PER_SEC;

	}
	//cerr << "Grand total " << setprecision(10) << ( clock() - start ) / (double) CLOCKS_PER_SEC << " IO " << total_io << endl;
	//cerr << "init " << total_init << " do " << total_do << " comp " << total_comp << " ins " << total_insert << " lookup " << total_lookup << endl;
}