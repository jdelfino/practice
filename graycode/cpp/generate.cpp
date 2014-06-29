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

using namespace std;
using namespace std::placeholders;

typedef unordered_map<int, vector<string>> Cache;
typedef function<string(int, int)> ComputeFunc;

string iterative_find(int n, int c){
	string rval;

	int orig_c = c;
	while(n > 1){
		if(c >= pow(2, n-1)){
			rval += "1";
			c = pow(2,n) - 1 - c;
		} else {
			rval += "0";
		}
		n = n - 1;
	}
	return rval + to_string(c);
}

vector<string> generate(int n, Cache *cache = nullptr){
	if(cache) {
		auto cached = cache->find(n);
		if(cached != cache->end()){ 
			return cached->second;
		}
	}

	if(n < 1) {
		throw exception();
	}

	if(n == 1){
		return vector<string>{"0","1"};
	}

	auto recurse = generate(n-1, cache);
	auto rval = recurse;
	std::reverse(recurse.begin(), recurse.end());
	rval.insert(rval.end(), recurse.begin(), recurse.end());

	for(int i = 0; i < (rval.size() / 2); ++i){
		rval[i] = '0' + rval[i];
	}

	for(int i = rval.size() - 1; i >= rval.size() / 2; --i){
		rval[i] = '1' + rval[i];
	}

	if(cache){
		(*cache)[n] = rval;
	}

	return rval;
}

string brute_generate(int n, int c, Cache *cache = nullptr){
	auto full = generate(n, cache);
	return full[c];
}

string timeit(double &accum, ComputeFunc func, int n, int c) {
    std::clock_t start = std::clock();
    auto rval = func(n, c);
    accum += ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
    return rval;
}

string testit(int, int) { return ""; }

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
			timeit(timer, item.second, n, c);
			times[item.first] = timer;
		}
	}

	for(const auto &time : times){
		cout << time.first << " took: " << std::fixed << std::setprecision(3) << time.second << "s" << endl;
	}
}
