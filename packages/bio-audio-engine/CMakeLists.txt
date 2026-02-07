cmake_minimum_required(VERSION 3.15)
project(bio_audio_engine)

# Use N-API wrapper for C++
add_definitions(-DNAPI_CPP_EXCEPTIONS)

# Include Node-API headers
include_directories(${CMAKE_JS_INC})

# Source files
file(GLOB SOURCE_FILES "src/*.cpp" "src/*.h")

# Define the shared library (Node addon)
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})

# Properties for Node.js addon
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "" SUFFIX ".node")

# Link libraries (if any, e.g., external audio libs later)
target_link_libraries(${PROJECT_NAME} ${CMAKE_JS_LIB})

if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /EHsc)
else()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -fPIC)
endif()
