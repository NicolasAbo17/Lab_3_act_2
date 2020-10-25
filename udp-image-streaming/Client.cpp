/*
 *   C++ UDP socket client for live image upstreaming
 *   Modified from http://cs.ecs.baylor.edu/~donahoo/practical/CSockets/practical/UDPEchoClient.cpp
 *   Copyright (C) 2015
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "PracticalSocket.h"      // For UDPSocket and SocketException
#include <iostream>               // For cout and cerr
#include <cstdlib>                // For atoi()
#include <chrono>
#include <thread>
using namespace std;

#include "opencv2/opencv.hpp"
using namespace cv;
#include "config.h"
#define BUF_LEN 65540


void videoStreaming(unsigned short servPort, string servAddress,string movie, unsigned char multicastTTL){
	cout << movie << "\n";
	try {
		UDPSocket sock;
		sock.setMulticastTTL(multicastTTL);
		int jpegqual =  ENCODE_QUALITY; // Compression Parameter
		char buffer[BUF_LEN];
		Mat frame, send;
		vector < uchar > encoded;

		clock_t last_cycle = clock();
		while(1){
			VideoCapture cap(movie); // Grab the camera
			if (!cap.isOpened()) {
				cerr << "OpenCV Failed to open camera";
				exit(1);
			}
			while (1) {
				cap >> frame;
				if(frame.size().width==0)break;//simple integrity check; skip erroneous data...
				resize(frame, send, Size(FRAME_WIDTH, FRAME_HEIGHT), 0, 0, INTER_LINEAR);
				vector < int > compression_params;
				compression_params.push_back(IMWRITE_JPEG_QUALITY);
				compression_params.push_back(jpegqual);

				imencode(".jpg", send, encoded, compression_params);
				int total_pack = 1 + (encoded.size() - 1) / PACK_SIZE;
			   
				sock.sendTo( & encoded[0], PACK_SIZE, servAddress, servPort);
				waitKey(FRAME_INTERVAL);
				clock_t next_cycle = clock();
				double duration = (next_cycle - last_cycle) / (double) CLOCKS_PER_SEC;
				cout << movie << "\teffective FPS:" << (1 / duration) << " \tkbps:" << (PACK_SIZE * total_pack / duration / 1024 * 8) << endl;

				cout << next_cycle - last_cycle;
				last_cycle = next_cycle;
			}
		// Destructor closes the socket
		}

	} catch (SocketException & e) {
		cerr << e.what() << endl;
		exit(1);
	}
}


//Main function
int main(int argc, char * argv[]) {
	
	int films = atoi(argv[1]);

	string movies[] = {"car-detection.mp4","bolt-detection.mp4"};
	
	unsigned int ports[] = {10020,10021};
	
	string addresses[] = {"224.0.0.0","224.0.0.1"};

	vector<thread> threads;
	
	for(int i = 0; i < films;++i){
		threads.push_back(thread(videoStreaming,ports[i],addresses[i],movies[i],1));
	}
	for(auto &th : threads)
		th.join();
	
    return 0;
}
