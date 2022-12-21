#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstdio>

#include "Shape.h"
#include "bitmap_image.hpp"

using std::cout;
using std::cerr;
using std::endl;


int getX(const double &lon){
    const int width = 23040;  // the conversion equation from lat/lon to x/y is tiny, so this is the ratio scaled up
    const double x = fmod((width*(180 + lon)/360), (width + (width/2)));
    return (int)round(x) - 4850;  // shift transformation to make it fit within the frame
}

int getY(const double &lat){
    const double width = 23040;  // the conversion equation from lat/lon to x/y is tiny, so this is the ratio scaled up
    const double height = 15360;  // the conversion equation from lat/lon to x/y is tiny, so this is the ratio scaled up
    const double PI = 3.14159265359;
    const double latRad = lat*PI/180;
    const double mercN = log(tan((PI/4)+(latRad/2)));
    const double y = (height/2)-(width*mercN/(2*PI));
    return (int)round(y) - 5000;  // shift transformation to make it fit within the frame
}

void draw_image(const std::vector<std::vector<std::vector<double>>> &shapes){
    bitmap_image image(720,480);
    image.set_all_channels(255,255,255);
    image_drawer draw(image);
    draw.pen_width(1);
    draw.pen_color(255, 0, 0);

    // Render shapes to window
    for (std::vector<std::vector<double>> points: shapes){
        for (int i = 0; i < points.size() - 1; i++){
            std::vector<double> &pair1 = points.at(i);
            std::vector<double> &pair2 = points.at(i+1);
            const int x1 = getX(pair1.front());
            const int y1 = getY(pair1.back());
            const int x2 = getX(pair2.front());
            const int y2 = getY(pair2.back());
            draw.line_segment(x1,y1,x2,y2);
        }
    }
    image.save_image("/base/images/output.png");
}

void read_vol(const std::string fn) {
}

int main() {
    std::vector<std::vector<std::vector<double>>> shps;
    Shape shape("../data/okcounties.shp");
    shps = shape.get_shapes();
    draw_image(shps);
    if (remove("/src/vol/healthcheck.txt") != 0) {
        cerr << "/src/vol/healthcheck.txt could not be deleted" << endl;
    }
    else {
        cout << "/src/vol/healthcheck.txt successfully deleted" << endl;
    }
    return 0;
}
