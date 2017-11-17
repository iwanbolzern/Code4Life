import signal
from enum import Enum

import os
from subprocess import Popen, PIPE

from src.data_holder import Location

N = 2
Debug_AI = False
Timeout = False
PIPE_READ = 0
PIPE_WRITE = 1
FirstTurnTime = 1*(1 if Timeout else 10)
TimeLimit = 0.1 * (1 if Timeout else 10)

stop = False


LocationToString = ["SAMPLES", "DIAGNOSIS", "MOLECULES", "LABORATORY", "START_POS"]
StrToLocation = {"SAMPLES": Location.SAMPLES, "DIAGNOSIS": Location.DIAGNOSIS, "MOLECULES": Location.MOLECULES, "LABORATORY": Location.LABORATORY}
intToLocation = {0: Location.SAMPLES, 1: Location.DIAGNOSIS, 2: Location.MOLECULES, 3: Location.LABORATORY}
typeToStr = ["A", "B", "C", "D", "E"]
TypeToInt = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
Distances = [[0,3,3,3], [3,0,3,4], [3,3,0,3], [3,4,3,0], [2,2,2,2]] #Distances from everywhere to everywhere

class SampleTemplate:
    def __init__(self):
        self.cost = [] * 5;
        self.score = None
        self.exp = None



class Sample(SampleTemplate):
    def __init__(self):
        self.diagnosed=False
        self.id = None
        self.rank = None
        self.owner = None

struct player{
    location r;
    int eta,score;
    array<int,5> Mol,Exp;
    vector<sample> Samp;
};

struct project{
    array<int,5> Target;
};

const vector<project> ProjectList{
    { 3, 3, 0, 0, 3 },
    { 0, 3, 3, 3, 0 },
    { 3, 0, 0, 3, 3 },
    { 0, 0, 4, 4, 0 },
    { 0, 4, 4, 0, 0 },
    { 0, 0, 0, 4, 4 },
    { 4, 0, 0, 0, 4 },
    { 3, 3, 3, 0, 0 },
    { 0, 0, 3, 3, 3 },
    { 4, 4, 0, 0, 0 }
};

struct state{
    int SampleCount;
    array<player,2> P;
    array<int,5> Avail;
    vector<project> Proj;
    vector<sample> Samp;
    array<list<sample_template>,3> SamplePool;
};

struct action{
    action_type type;
    int id;
};

inline string EmptyPipe(const int fd){
    int nbytes;
    if(ioctl(fd,FIONREAD,&nbytes)<0){
        throw(4);
    }
    string out;
    out.resize(nbytes);
    if(read(fd,&out[0],nbytes)<0){
        throw(4);
    }
    return out;
}

class AI:

    def __init__(self, process):
        self.process = None

    def stop(self):
        os.kill(self.pid, signal.SIGKILL)

    def feed_input(self, input):
        stdout_data = self.process.communicate(input=input)[0]


def start_process(start_cmd):
    p = Popen([start_cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    ai = AI(p)
    return ai

def get_move



inline bool IsValidMove(const state &S,const AI &Bot,const string &M){
    return count(M.begin(),M.end(),'\n')==1;
}

string GetMove(const state &S,AI &Bot,const int turn){
    pollfd outpoll{Bot.outPipe,POLLIN};
    time_point<system_clock> Start_Time{system_clock::now()};
    string out;
    while(static_cast<duration<double>>(system_clock::now()-Start_Time).count()<(turn==1?FirstTurnTime:TimeLimit) && !IsValidMove(S,Bot,out)){
        double TimeLeft{(turn==1?FirstTurnTime:TimeLimit)-static_cast<duration<double>>(system_clock::now()-Start_Time).count()};
        if(poll(&outpoll,1,TimeLeft)){
            out+=EmptyPipe(Bot.outPipe);
        }
    }
    return out;
}

inline bool Has_Won(const array<AI,N> &Bot,const int idx)noexcept{
    if(!Bot[idx].alive()){
        return false;
    }
    for(int i=0;i<N;++i){
        if(i!=idx && Bot[i].alive()){
            return false;
        }
    }
    return true;
}

inline bool All_Dead(const array<AI,N> &Bot)noexcept{
    for(const AI &b:Bot){
        if(b.alive()){
            return false;
        }
    }
    return true;
}

action StringToAction(const state &S,const string &M_Str,const int id){
    action M;
    stringstream ss(M_Str);
    string type;
    ss >> type;
    if(type=="WAIT"){
        M=action{GOTO,S.P[id].r};
    }
    else if(type=="GOTO"){
        string destination;
        ss >> destination;
        if(StrToLocation.find(destination)==StrToLocation.end()){//Invalid destination
            cerr << "Invalid destination: " << M_Str << endl;
            throw(3);
        }
        M=action{GOTO,StrToLocation.at(destination)};
    }
    else if(type=="CONNECT"){
        string type;
        ss >> type;
        if(TypeToInt.find(type)!=TypeToInt.end()){
            M=action{CONNECT,TypeToInt.at(type)};
        }
        else{
            try{
                M=action{CONNECT,stoi(type)};
            }
            catch(...){//Invalid connect, neither a type nor an id
                cerr << "Invalid CONNECT: " << M_Str << endl;
                throw(3);
            }
        }
    }
    else{//Invalid move
        cerr << "Invalid move: " << M_Str << endl;
        throw(3);
    }
    return M;
}

inline bool ValidMoleculeIndex(const int idx)noexcept{
    return idx>=0 && idx<=4;
}

inline bool ValidRank(const int rank)noexcept{
    return rank>0 && rank<=3;
}

bool ReadyToProduce(const player &p,const sample &s){
    if(!s.diagnosed){
        return false;
    }
    for(int i=0;i<5;++i){//Look for missing molecules
        if(p.Mol[i]<s.Cost[i]-p.Exp[i]){
            return false;
        }
    }
    return true;
}

bool Completed_Project(const player &p,const project &proj){
    for(int m=0;m<5;++m){
        if(p.Exp[m]<proj.Target[m]){
            return false;
        }
    }
    return true;
}

def play_game()

int Play_Game(const array<string,N> &Bot_Names,state &S){
    array<AI,N> Bot;
    for(int i=0;i<N;++i){
        Bot[i].id=i;
        Bot[i].name=Bot_Names[i];
        StartProcess(Bot[i]);
        stringstream ss;
        ss << S.Proj.size() << endl;
        for(int p=0;p<S.Proj.size();++p){//Project inputs
            for(int m=0;m<5;++m){
                ss << S.Proj[p].Target[m] << " ";
            }
            ss << endl;
        }
        Bot[i].Feed_Inputs(ss.str());
    }
    int turn{0};
    while(++turn>0 && !stop){
        array<action,N> M;
        for(int i=0;i<N;++i){
            if(Bot[i].alive()){
                stringstream ss;
                for(int j=0;j<2;++j){//Two player inputs
                    const player& p{S.P[(i+j)%2]};
                    ss << locationToStr[p.r] << " " << p.eta << " " << p.score;
                    for(int m=0;m<5;++m){
                        ss << " " << p.Mol[m];
                    }
                    for(int m=0;m<5;++m){
                        ss << " " << p.Exp[m];
                    }
                    ss << endl;
                }
                for(int m=0;m<5;++m){
                    ss << max(0,S.Avail[m]) << " ";
                }
                ss << endl;
                ss << S.Samp.size()+S.P[0].Samp.size()+S.P[1].Samp.size() << endl;
                for(const sample &s:S.Samp){
                    ss << s.id << " " << -1 << " " << s.rank << " " << typeToStr[s.exp] << " " << s.score;
                    for(int m=0;m<5;++m){
                        ss << " " << s.Cost[m];
                    }
                    ss << endl;
                }
                for(int j=0;j<2;++j){
                    const player& p{S.P[(i+j)%2]};
                    for(const sample &s:p.Samp){
                        ss << s.id << " " << j << " " << s.rank << " " << (s.diagnosed?typeToStr[s.exp]:"0") << " " << (s.diagnosed?s.score:-1);
                        for(int m=0;m<5;++m){
                            ss << " " << (s.diagnosed?s.Cost[m]:-1);
                        }
                        ss << endl;
                    }
                }
                try{
                    Bot[i].Feed_Inputs(ss.str());
                    string out=GetMove(S,Bot[i],turn);
                    //cerr << i << " " << out << endl;
                    M[i]=StringToAction(S,out,i);
                }
                catch(int ex){
                    if(ex==1){//Timeout
                        cerr << "Loss by Timeout of AI " << Bot[i].id << " name: " << Bot[i].name << endl;
                    }
                    else if(ex==3){
                        cerr << "Invalid move from AI " << Bot[i].id << " name: " << Bot[i].name << endl;
                    }
                    else if(ex==4){
                        cerr << "Error emptying pipe of AI " << Bot[i].name << endl;
                    }
                    else if(ex==5){
                        cerr << "AI " << Bot[i].name << " died before being able to give it inputs" << endl;
                    }
                    Bot[i].stop(turn);
                }
            }
        }
        Simulate(S,M);
        for(int i=0;i<N;++i){
            string err_str{EmptyPipe(Bot[i].errPipe)};
            if(Debug_AI){
                ofstream err_out("log.txt",ios::app);
                err_out << err_str << endl;
            }
        }
        for(int i=0;i<N;++i){
            if(Has_Won(Bot,i)){
                //cerr << i << " has won in " << turn << " turns" << endl;
                return i;
            }
        }
        if(All_Dead(Bot)){
            return -1;
        }
        if(turn==200){
            //cerr << S.P[0].score << " " << S.P[1].score << endl;
            return S.P[0].score==S.P[1].score?-1:S.P[0].score>S.P[1].score?0:1;
        }
    }
    return -2;
}

int Play_Round(array<string,N> Bot_Names){
    default_random_engine generator(system_clock::now().time_since_epoch().count());
    uniform_int_distribution<int> Swap_Distrib(0,1);
    const bool player_swap{Swap_Distrib(generator)==1};
    if(player_swap){
        swap(Bot_Names[0],Bot_Names[1]);
    }
    //Initial state generation
    state S;
    for(player &p:S.P){
        p=player{START,0,0,{0,0,0,0,0},{0,0,0,0,0},{}};
    }
    for(int &m:S.Avail){
        m=5;//5 molecules per type
    }
    array<vector<sample_template>,3> Pool_Vec=SampleList;
    for(int i=0;i<3;++i){
        random_shuffle(Pool_Vec[i].begin(),Pool_Vec[i].end());
        copy(Pool_Vec[i].begin(),Pool_Vec[i].end(),back_inserter(S.SamplePool[i]));
    }
    vector<project> Projects=ProjectList;
    random_shuffle(Projects.begin(),Projects.end());
    for(int i=0;i<3;++i){
        S.Proj.push_back(Projects[i]);
    }
    S.SampleCount=0;

    int winner{Play_Game(Bot_Names,S)};
    if(player_swap){
        return winner==-1?-1:winner==0?1:0;
    }
    else{
        return winner;
    }
}

void StopArena(const int signum){
    stop=true;
}

int main(int argc,char **argv){
    if(argc<3){
        cerr << "Program takes 2 inputs, the names of the AIs fighting each other" << endl;
        return 0;
    }
    int N_Threads{1};
    if(argc>=4){//Optional N_Threads parameter
        N_Threads=min(2*omp_get_num_procs(),max(1,atoi(argv[3])));
        cerr << "Running " << N_Threads << " arena threads" << endl;
    }
    array<string,N> Bot_Names;
    for(int i=0;i<2;++i){
        Bot_Names[i]=argv[i+1];
    }
    cout << "Testing AI " << Bot_Names[0];
    for(int i=1;i<N;++i){
        cerr << " vs " << Bot_Names[i];
    }
    cerr << endl;
    for(int i=0;i<N;++i){//Check that AI binaries are present
        ifstream Test{Bot_Names[i].c_str()};
        if(!Test){
            cerr << Bot_Names[i] << " couldn't be found" << endl;
            return 0;
        }
        Test.close();
    }
    signal(SIGTERM,StopArena);//Register SIGTERM signal handler so the arena can cleanup when you kill it
    signal(SIGPIPE,SIG_IGN);//Ignore SIGPIPE to avoid the arena crashing when an AI crashes
    int games{0},draws{0};
    array<double,2> points{0,0};
    #pragma omp parallel num_threads(N_Threads) shared(games,points,Bot_Names)
    while(!stop){
        int winner{Play_Round(Bot_Names)};
        if(winner==-1){//Draw
            #pragma omp atomic
            ++draws;
            #pragma omp atomic
            points[0]+=0.5;
            #pragma omp atomic
            points[1]+=0.5;
        }
        else{//Win
            ++points[winner];
        }
        #pragma omp atomic
        ++games;
        double p{static_cast<double>(points[0])/games};
        double sigma{sqrt(p*(1-p)/games)};
        double better{0.5+0.5*erf((p-0.5)/(sqrt(2)*sigma))};
        #pragma omp critical
        cout << "Wins:" << setprecision(4) << 100*p << "+-" << 100*sigma << "% Rounds:" << games << " Draws:" << draws << " " << better*100 << "% chance that " << Bot_Names[0] << " is better" << endl;
    }
}