#include <iostream>
#include <vector>
#include <exception> 
#include <algorithm>
#include <cmath>
#include <functional>
#include <iomanip>
#include <cassert>
#include <unordered_map>
#include <set>
#include <sstream>

using namespace std;
using namespace std::placeholders;

typedef vector<string> ValType;
typedef unordered_map<int, ValType> Cache;
typedef function<string(int, int)> ComputeFunc;

const int powers[]{
	int(pow(2,0)),
	int(pow(2,1)),
	int(pow(2,2)),
	int(pow(2,3)),
	int(pow(2,4)),
	int(pow(2,5)),
	int(pow(2,6)),
	int(pow(2,7)),
	int(pow(2,8)),
	int(pow(2,9)),
	int(pow(2,10)),
	int(pow(2,11)),
	int(pow(2,12)),
	int(pow(2,13)),
	int(pow(2,14)),
	int(pow(2,15)),
	int(pow(2,16)),
	int(pow(2,17)),
	int(pow(2,18)),
	int(pow(2,19)),
	int(pow(2,20)),
	int(pow(2,21)),
	int(pow(2,22)),
	int(pow(2,23)),
	int(pow(2,24)),
	int(pow(2,25)),
	int(pow(2,26))
};

inline string iterative_find(int n, int c){
	int orig_n = n;
	string rval(n, '0');

	while(n > 1){
		//cerr << "n " << n << " c "  << c << endl;
		if(c >= powers[n-1]) {
			rval[orig_n - n] = '1';
			//cerr << "flipping the bit " << rval << endl;
			c = powers[n] - 1 - c;
		} 
		--n;
	}
	rval[orig_n-1] = c ? '1' : '0';
	return rval;
}

void generate(int n, ValType& vals, Cache *cache = nullptr){
	//cerr << "generate " << n << " " << vals.size() << endl;
	
	if(cache) {
		auto cached = cache->find(n);
		if(cached != cache->end()){ 
			return;
		}
	}
	
	if(n < 1) {
		throw exception();
	}

	if(n == 1){
		vals[0] = "0";
		vals[1] = "1";
	} else {

		generate(n-1, vals, cache);
		int tn = pow(2,n)-1;
		int tnmo = pow(2,n-1);
		for(int i = 0; i < tnmo; ++i){
			vals[i] = "0" + vals[i];
			vals[tn - i] = "1" + vals[i];
		}
	}

	if(cache){
  		(*cache)[n] = vals;
	}
}

string brute_generate(int n, int c, Cache *cache = nullptr){
	// check first to avoid an allocation
	if(cache) {
		auto cached = cache->find(n);
		if(cached != cache->end()){ 
			//cerr << "using cache " << n << endl;
			return cached->second[c];
		}
	}

	ValType vals(pow(2,n));
	generate(n, vals, cache);
	return cache->find(n)->second[c];
}

string timeit(double &accum, ComputeFunc func, int n, int c) {
    std::clock_t start = std::clock();
    auto rval = func(n, c);
    accum += ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
    return rval;
}

int main(int argc, char** argv){
	cout << "Hello World" << endl;
	double brute_time = 0.0;
	double find_time = 0.0;

	Cache cache;
	unordered_map<string, ComputeFunc> funcs;
	//funcs["brute"] = brute_generate;
	funcs["find"] = iterative_find;
	funcs["brute cached"] = bind(brute_generate, _1, _2, &cache);

	unordered_map<string, double> times;

	if(string(argv[1]) == "test"){
		int max = atoi(argv[2]);
		for(const auto& item : funcs) {
			double timer = 0.0;
			for(int n = 1; n < max; ++n){
				cout << "Testing " << n << endl;
				for(int c = 0; c < pow(2,n); ++c){
					timeit(timer, item.second, n, c);
				}
			}
			times[item.first] = timer;
		}
	} else {
		int n = atoi(argv[1]);
		int c = atoi(argv[2]);
		for(const auto& item : funcs) {
			double timer = 0.0;
			auto res = timeit(timer, item.second, n, c);
			times[item.first] = timer;
			cout << item.first << " " << res << endl;
		}
	}

	for(const auto &time : times){
		cout << time.first << " took: " << std::fixed << std::setprecision(3) << time.second << "s" << endl;
	}
}
