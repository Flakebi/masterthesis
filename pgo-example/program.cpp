#include <iostream>
#include <fstream>

int main(int argc, char *argv[]) {
	if (argc != 2) {
		std::cout << "Usage: ./test <inputfile>\n";
		return 1;
	}
	std::ifstream in(argv[1]);
	if (!in.is_open()) {
		std::cout << "Failed to open " << argv[1] << "\n";
		return 1;
	}
	std::string s;
	in >> s;
	std::cout << s;
	return 0;
}
