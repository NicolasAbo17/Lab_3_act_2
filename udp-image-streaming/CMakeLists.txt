cmake_minimum_required(VERSION 2.8)
project( lan_vid_pseudostream )
find_package( OpenCV REQUIRED )
add_executable( server Server.cpp PracticalSocket.cpp )
target_link_libraries( server ${OpenCV_LIBS} )
add_executable( client Client.cpp PracticalSocket.cpp )
target_link_libraries( client ${OpenCV_LIBS} )
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
