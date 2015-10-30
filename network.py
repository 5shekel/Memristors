__author__ = 'nfrik'

import networkx as nx;
import matplotlib.pylab as plt;
import random
from ahkab import new_ac, new_op, run
from ahkab.circuit import Circuit
import memristor;



#Get first voltage values
def set_mem_voltages(r):
    for k in memdict.keys():
        [n0,n1]=['VN'+str(memdict[k][0]),'VN'+str(memdict[k][1])];
        [v0,v1]=[r.results[n0],r.results[n1]]
        memdict[k][2].setV(v1-v0)

def update_circ_res_vals():
    global n
    for k in memdict.keys():
        memdict[k][2].updateW();
        for n in range(len(cir)):
            if k == cir[n].part_id:
                cir[n].value = memdict[k][2].getR();


def update_mem_state():
    for k in memdict.keys():
        memdict[k][2].updateW();


w=0.1
D=1.0
Roff=10.;
Ron=1.;
mu=10.
Tao=0.01

G=nx.random_regular_graph(3,40)

#create circuit
cir = Circuit('Memristor test')

#dict with terminals and memristors
memdict={}
for e in G.edges_iter():
    rval=round(Roff+0.01*Roff*(random.random()-0.5),2);
    key='R'+str(e[0])+str(e[1])
    [v1,v2]=[e[0],e[1]]
    memdict[key]=[v1,v2,memristor.memristor(w,D,Roff,Ron,mu,Tao,0.0)] # we set v=0 value temporarily
    cir.add_resistor(key,'n'+str(v1),'n'+str(v2),rval)
    G[e[0]][e[1]]['weight']=rval;
    # edge_labels[e]=rval;

for n in G.nodes_iter():
    G.node[n]['number']=n;


#Choose randomly ground and voltage terminal nodes on graph
[v1,gnd]=random.sample(xrange(0,len(G.nodes())),2);
lastnode=len(G.nodes());
G.add_edge(v1,lastnode);
G.node[lastnode]['number']='V1';
lastnode+=1;
G.add_edge(gnd,lastnode);
G.node[lastnode]['number']='gnd';

edge_labels=nx.get_edge_attributes(G,'weight')
node_labels=nx.get_node_attributes(G,'number')

# fig,ax = plt.subplots()
# pos=nx.circular_layout(G)
# nx.draw(G,pos=pos,ax=ax)
# nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_labels,font_size=8,ax=ax)
# nx.draw_networkx_labels(G,pos=pos,labels=node_labels,font_size=8,ax=ax)
#
# plt.savefig('show.png')
# plt.show()



cir.add_resistor("RG",'n'+str(gnd),cir.gnd,0.001);
cir.add_vsource("V1",'n'+str(v1),cir.gnd,100);
opa = new_op();

#get initial voltages
# set_mem_voltages(r);

# memdict_t={}



cur=[]
for i in range(100):
    r = run(cir,opa)['op'];
    set_mem_voltages(r)
    update_mem_state()
    update_circ_res_vals()
    cur.append(r)

plt.plot([x.results['I(V1)'] for x in cur])
plt.show()

# #Get first voltage values
# keys=r.results.keys();
# keys.remove('I(V1)'); #for now we know this key


#create memristors list
# mems={};
# for k in keys:
#     curv=r.results[k];
#     mems[k]=memristor.memristor(w,D,Roff,Ron,mu,Tao,curv);

#connect

# #evolve the system
# for i in range(1000):
# #update circuit resistor values
#     for k in keys:
#         cir.get_elem_by_name(k).
# #calculate circuit
# #update voltages on memristors
# #save values from memristors

# print mems;

# print r

