import copy
from data_holder import State, Move

#SAMPLES	DIAGNOSIS	MOLECULES	LABORATORY  Start area
#SAMPLES	0	3	3	3   2
#DIAGNOSIS	3	0	3	4   2
#MOLECULES	3	3	0	3   2
#LABORATORY	3	4	3	0   2
#Start area	2	2	2	2   0
from src.data_holder import Robot, Action, Location

movement_matrix = [[0,3,3,3,2],
                   [3,0,3,4,2],
                   [3,3,0,3,2],
                   [3,4,3,0,2],
                   [2,2,2,2,0]]

def simulate_action(state: State, my_action: Move, enemy_action: Move) -> State:
    """ Returns new game state after both actions are performed
    :param state:
    :param my_action:
    :param enemy_action:
    """

    state_before = copy.deepcopy(state)

def simulate_player(state: State, player: Robot, move: Move):
    if player.eta == 0:
        if move.action == Action.GOTO:
            player.eta = movement_matrix[player.target][move.arg]
            player.target = move.arg
        else:
            if player.target == Location.SAMPLES and move.arg in [1,2,3]:


void Simulate(state &S,const array<action,N> &M){
    const state S_before=S;
    for(int i=0;i<2;++i){
        player& p{S.P[i]};
        const action& mv{M[i]};
        if(p.eta==0){//Ignore actions of moving players
            if(mv.type==GOTO){
                p.eta=Distances[p.r][mv.id];
                p.r=intToLocation[mv.id];
            }
            else{//Connect
                if(p.r==SAMPLES && ValidRank(mv.id)){//Take undiagnosed sample
                    const int& rank{mv.id};
                    S.SamplePool[rank-1].push_back(S.SamplePool[rank-1].front());//Make a copy of the taken sample at the back of the list
                    sample s=S.SamplePool[rank-1].front();
                    S.SamplePool[rank-1].pop_front();
                    s.id=S.SampleCount++;
                    s.rank=rank;
                    s.diagnosed=false;
                    s.owner=i;
                    p.Samp.push_back(s);
                }
                else if(p.r==MOLECULES && ValidMoleculeIndex(mv.id)){//Take molecule
                    if(S_before.Avail[mv.id]>0 && accumulate(p.Mol.begin(),p.Mol.end(),0)<10){
                        --S.Avail[mv.id];
                        ++p.Mol[mv.id];
                    }
                }
                else if(p.r==LABORATORY && find_if(p.Samp.begin(),p.Samp.end(),[&](const sample &s){return s.id==mv.id;})!=p.Samp.end()){
                    const auto s=find_if(p.Samp.begin(),p.Samp.end(),[&](const sample &s){return s.id==mv.id;});
                    if(ReadyToProduce(p,*s)){
                        for(int m=0;m<5;++m){
                            const int spent{max(0,s->Cost[m]-p.Exp[m])};
                            p.Mol[m]-=spent;
                            S.Avail[m]+=spent;
                        }
                        p.score+=s->score;//Increase score
                        ++p.Exp[s->exp];//Gain expertise
                        p.Samp.erase(s);
                    }
                    else{
                        cerr << i << " tried to produce something he can't" << endl;
                    }
                }
                else if(p.r==DIAGNOSIS){
                    const auto player_s{find_if(p.Samp.begin(),p.Samp.end(),[&](const sample &s){return s.id==mv.id;})};
                    const auto diag_s{find_if(S.Samp.begin(),S.Samp.end(),[&](const sample &s){return s.id==mv.id;})};
                    if(player_s!=p.Samp.end()){
                        if(player_s->diagnosed){
                            S.Samp.push_back(*player_s);
                            p.Samp.erase(player_s);
                        }
                        else{
                            player_s->diagnosed=true;
                        }
                    }
                    else if(diag_s!=S.Samp.end()){
                        const action mv2{M[(i+1)%2]};
                        const player& p2{S.P[(i+1)%2]};
                        const bool other_hasnt_requested{mv.id!=mv2.id || mv.type!=mv2.type || p2.r!=DIAGNOSIS || p2.eta>0 || p2.Samp.size()==3};
                        if(p.Samp.size()<3 && (diag_s->owner==i || other_hasnt_requested) ){
                            //cerr << "Player " << i << " got sample " << mv.id << endl;
                            p.Samp.push_back(*diag_s);
                            S.Samp.erase(diag_s);
                        }
                    }
                }
            }
        }
    }
    for(int i=0;i<2;++i){//Decrease eta of both players
        player& p{S.P[i]};
        p.eta=max(0,p.eta-1);
    }
    for(auto it=S.Proj.begin();it!=S.Proj.end();){
        bool completed{false};
        for(int i=0;i<2;++i){
            if(Completed_Project(S.P[i],*it)){
                //cerr << "Player " << i << " completed a project" << endl;
                S.P[i].score+=50;
                completed=true;
            }
        }
        if(completed){
            it=S.Proj.erase(it);
        }
        else{
            ++it;
        }
    }
}