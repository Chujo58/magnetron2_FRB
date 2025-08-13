# Put the directory above 'DNest4' into an environment variable
# called DNEST4_PATH for this to work.
DNEST4_PATH = /arc/home/clegue
JSON_PATH = ../include
GSL_PATH = /opt/conda/include
BLAS_PATH = /opt/conda/lib

CXXFLAGS = -std=c++11 -O3 -Wall -Wextra -pedantic -DNDEBUG
LIBS = -ldnest4 -lpthread -lgsl -lopenblas

default:
	g++ -I$(GSL_PATH) -I$(DNEST4_PATH) -I$(JSON_PATH) $(CXXFLAGS) -c *.cpp
	g++ -L$(BLAS_PATH) -L$(DNEST4_PATH)/DNest4/code -o main *.o $(LIBS)
	rm *.o

