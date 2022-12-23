//
// Created by adam slay on 12/13/22.
//
#include <vector>
#ifndef PNG_MAPPER_EXE_CSVREADER_H
#define PNG_MAPPER_EXE_CSVREADER_H


class CSVReader {
public:
    std::vector<std::vector<std::string>> parse_csv(const std::string& fn);
};


#endif //PNG_MAPPER_EXE_CSVREADER_H
