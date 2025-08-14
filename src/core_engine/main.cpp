
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

// Platform-specific includes for binary I/O
#ifdef _WIN32
#include <io.h>
#include <fcntl.h>
#endif

// In a real-world scenario, this buffer size would be tuned for performance.
const size_t BUFFER_SIZE = 8192;

void capture(const std::string& source_path) {
    // Set stdout to binary mode on Windows
    #ifdef _WIN32
    _setmode(_fileno(stdout), _O_BINARY);
    #endif

    std::ifstream source(source_path, std::ios::binary);
    if (!source) {
        std::cerr << "Error: Could not open source file " << source_path << std::endl;
        exit(1);
    }

    std::vector<char> buffer(BUFFER_SIZE);
    while (source.read(buffer.data(), buffer.size())) {
        std::cout.write(buffer.data(), source.gcount());
    }
    // Write the last partial chunk if it exists
    if (source.gcount() > 0) {
        std::cout.write(buffer.data(), source.gcount());
    }
}

void restore(const std::string& dest_path) {
    // Set stdin to binary mode on Windows
    #ifdef _WIN32
    _setmode(_fileno(stdin), _O_BINARY);
    #endif

    std::ofstream dest(dest_path, std::ios::binary | std::ios::trunc);
    if (!dest) {
        std::cerr << "Error: Could not open destination file " << dest_path << std::endl;
        exit(1);
    }

    std::vector<char> buffer(BUFFER_SIZE);
    while (std::cin.read(buffer.data(), buffer.size())) {
        dest.write(buffer.data(), std::cin.gcount());
    }
    // Write the last partial chunk if it exists
    if (std::cin.gcount() > 0) {
        dest.write(buffer.data(), std::cin.gcount());
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <capture|restore> <file_path>" << std::endl;
        return 1;
    }

    std::string mode = argv[1];
    std::string path = argv[2];

    if (mode == "capture") {
        capture(path);
    } else if (mode == "restore") {
        restore(path);
    } else {
        std::cerr << "Invalid mode. Use 'capture' or 'restore'." << std::endl;
        return 1;
    }

    return 0;
}
