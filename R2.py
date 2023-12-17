import networkx as nx
import random
import matplotlib.pyplot as plt
import os,sys
class uber:
    def GenerateGraph(self,a,b,c,d,e,f):
        """
        This function takes below arguments and returns a Graph object
        Args:
            a (int): seed value
            b (int):number of nodes in the graph 
            c (int):probability for edge creation 
            d (int):vechile count
            e (int):vechile capacity
            f (int):total number of clock ticks

        Returns:
            networkx.classes.graph.Graph
        """
        try:
            seed=a           
            self.n=b
            self.p=c
            self.vechile_count=d
            self.vechile_capacity=e
            self.total_clock_ticks=f
            G= nx.gnp_random_graph (self.n,p=self.p, seed=seed)       
            print ( G.nodes() )
            return G
        except Exception as e:
            raise e
    def generate_connected_graph(self,a,b,d,e,f):
        """
        This function creates a fully connected graph
        and prints the value of probability for edge creation  for the following nodes
          Args:
            a (int): seed value
            b (int):number of nodes in the graph 
            c (int):probability for edge creation 
            d (int):vechile count
            e (int):vechile capacity
            f (int):total number of clock ticks

        Returns:
            networkx.classes.graph.Graph
        """
        try:
            k=3
            c = k / (b - 1)  
            f1 = 0
            while f1 == 0:
                G = self.GenerateGraph(a, b, c, d, e, f)
                if nx.is_connected(G):
                    print("p:", c)
                    return G
                c += 0.01   
        except Exception as e:
            raise  e        
    def Add_weights_to_graph(self,weights,G):
        """
        This function creates edges between the nodes and assign weights to those edges
        Args:
            weights (list):In this list we have values stored in namedtuple which takes three values staring node,ending node,weight of the edge 
            G (Graph object):Graph object

        Returns:
            networkx.classes.graph.Graph
            _
        """
        try:
            if weights==None:
                for u, v in G.edges:
                    G.add_edge(u, v, weight=round(random.random(),1))
            else:
                for u,v,w in weights:
                    G.add_edge(u,v,weight=w)
            return G
        except Exception as e:
            raise e 
    def get_shortest_distance(self,G,a,b):
        """
        This function takes starting node and ending node and return shortest distance between them
        Args:
            G (Graph object):Graph object
            a (Node):starting node
            b (Node): ending node

        Returns:
            float number 
        """
        try:
            return nx.astar_path_length(self.G,a,b)
        except Exception as e:
            raise e
    def get_next_node(self,G,a,b):
        """
        return the nextnode the van is going to take
        Args:
            G (Graph object)
            a (Node)
            b (Node)

        Returns:
            node
        """
        try:
            shortest_path=nx.astar_path(G,a,b)
            if(len(shortest_path)==1):
                return shortest_path[0]
            else:
                return shortest_path[1]
        except Exception as e:
            raise  e
    def check(self,b):
        """
        It checks the capacity of the vechile that the current vechile can take a new customer or not
        Args:
            b (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:    
            capacity=self.e
            if self.no_of_passengers[b]<capacity:
                return 1
            else:
                return 0
        except Exception as e:
            raise  e    
    def Assign_values(self,a,b):
        """
          It takes pickup point and vechile list as argument and return the minimum distance and vechile to be assigned as output
        Args:
            a (Node): PickupNode
            b (list): vechilesnumber
        Returns:
            int,int
        """
        try:
            curr_distance=float('inf')
            vechile_number=None
            count=0
            passengers=6
            for i in range(b):
                if self.check(i)==1:
                    l=self.curr_vechile_location[i]
                    distance=self.get_shortest_distance(self.G,a,l)
                    if curr_distance>distance:
                        curr_distance=distance
                        vechile_number=i
                        passengers=self.no_of_passengers[i]
                    if curr_distance==distance:
                        if self.no_of_passengers[i]<passengers:
                            passengers=self.no_of_passengers[i]
                            curr_distance=distance
                            vechile_number=i       
                    #print(vechile_number,"joijoijo")        
                        
            if curr_distance==float('inf'):
                print("No vans are available, try again in 15 minutes")
                return -1,None
            else:                  
                return curr_distance,vechile_number
        except Exception as e:
            raise  e    
    def rearrange(self,a):
        """
        It rearranges the vechile list according to vechile current location
        Args:
            a (_type_):vechile_no

        Returns:
            list
        """
        try:
            dict1={}
            count=0
            for i in self.vechile_list[a]:
                dict1[count]=i
                count=count+1
            q=list(dict1[0].keys())[0]
            q1=dict1[0]
            w=q1[q][0]
            list4=[]
            if w==-1:
                list4.append(dict1[0])
                dict1.pop(0)
            v=self.curr_vechile_location[a]
            while len(dict1)>0:
                curr_key=None
                distance=float('inf')
                curr_value=None
                for i in dict1:
                    key=list(dict1[i].keys())[0]
                    dict2=dict1[i]
                    value=dict2[key][0]
                    temp=self.get_shortest_distance(self.G,v,value)
                    if temp<distance:
                        curr_key=i
                        curr_value=value
                        distance=temp
                list4.append(dict1[curr_key])
                v=curr_value
                dict1.pop(curr_key)
            #print(list4)
            return list4
        
        except Exception as e:
            raise  e
    def update(self):
        """
        updates the position of vechiles in each clock tick
        """
        try:
            for i in range(self.d):
                if len(self.vechile_list[i])>=1:
                    curr_customer=self.vechile_list[i][0]
                    key=list(curr_customer.keys())[0]
                    pick_up=curr_customer[key][0]
                    index=0
                    if pick_up==-1:
                        index=1
                    #print(" dd",index)    
                    loc=curr_customer[key][index] 
                      # print("eeee",index)
                    curr_loc=self.curr_vechile_location[i]    
                       # print(i," ,",curr_loc)
                       # print(loc)
                    new_loc=self.get_next_node(self.G,curr_loc,loc)
                    self.vechile_travelled[i].append(new_loc)
                    travel_dist=self.get_shortest_distance(self.G,curr_loc,loc)
                    self.curr_vechile_location[i]=new_loc
                    self.vechile_travel_distance[i]=self.vechile_travel_distance[i]+travel_dist 
                
        except Exception as e:
            raise  e       
    def TakeRideRequests(self,G):
        """
        This function takes G as input and checks if a new request is made if made add it to its near vechile list and rearrange priorities of the vechile
        """
        try: 
            for i in range(2):
                cust_id="customer"+str(self.count)
                self.count=self.count+1
                pick_up=self.cust_list[0][0]
                drop=self.cust_list[0][1]
                self.cust_list.pop(0)
               # print(self.cust_list)
                distance,vechile_no=self.Assign_values(pick_up,self.d)
                if distance==-1:
                    return -1
                self.no_of_trips=self.no_of_trips+1
                re={cust_id:[pick_up,drop]}
                re1=[(cust_id,'p',pick_up)]
                re2=[(cust_id,'d',drop)]
                self.vechile_track[vechile_no]=self.vechile_track[vechile_no]+re1+re2
                self.no_of_passengers[vechile_no]=self.no_of_passengers[vechile_no]+1
                self.vechile_list[vechile_no].append(re)
                if self.no_of_passengers[vechile_no]>1:
                    #print(self.curr_vechile_location[vechile_no])
                    self.vechile_list[vechile_no]=self.rearrange(vechile_no)
            self.update()
        except Exception as e:
            raise  e   
    def pick_customers(self):
        """
        This function will check if a vechile arrived at pickup location of customer and picks him up and it will update the current location of the vechile 
        """
        try:
            for i in range(self.d):
                curr_loc=self.curr_vechile_location[i]
                if len(self.vechile_list[i])>0:
                    #print(i)
                    curr_customer=self.vechile_list[i][0]
                    key=list(curr_customer.keys())[0]
                    pick_up=curr_customer[key][0]
                    if pick_up>=0:
                        if pick_up==curr_loc:
                            self.cus_dir[key]=[key,pick_up]
                            curr_customer[key][0]=-1
                            print("glob:",i)
                            curr_customer[key].append(self.vechile_travel_distance[i])
                            curr_customer[key].append(self.clock_ticks)
                            self.vechile_list[i][0]=curr_customer
                           # print("vechile",i,":",self.curr_vechile_location[i])
                            self.vechile_track[i].pop(0)          
        except Exception as e:
            raise  e                   
                    
    def drop_customers(self):
        """
        This function will check if a vechile is at the drop location if true remove the request from the vechilelist and it will update the current location of the vechile
        """
        try:
            for i in range(self.d):
                curr_loc=self.curr_vechile_location[i]
                if len(self.vechile_list[i])>0:
                    curr_customer=self.vechile_list[i][0]
                    key=list(curr_customer.keys())[0]
                    drop=curr_customer[key][1]
                    pick_up=curr_customer[key][0]
                    if pick_up==-1:
                        if drop==curr_loc:
                            self.cus_dir[key].append(curr_customer[key][1])
                            travel=self.vechile_travel_distance[i]-curr_customer[key][2]
                            time=self.clock_ticks-curr_customer[key][3]
                            self.cus_dir[key].append(travel)
                            self.cus_dir[key].append(time)
                            self.vechile_list[i].pop(0)
                            self.vechile_track[i].pop(0)
                        #print("vechile",i,":",self.curr_vechile_location[i])
                            self.no_of_passengers[i]=self.no_of_passengers[i]-1     
        except Exception as e:
            raise  e
    def intialize_vechile_track(self):
        """
        It takes number of vechiles as argument and returns a list where each vechile is intailized their starting position as 0
        Args:
            d (int):vechiles number

        Returns:
            list
        """
        try:
            list3=[]
            list4=[]
            for i in range(self.d):
                list4.append(list3)
            return list4
        except Exception as e:
            raise e 
            
                                                   
    def intialize_curr_location(self,d):
        """
        It takes number of vechiles as argument and returns a list where each vechile is intailized their starting position as 0
        Args:
            d (int):vechiles number

        Returns:
            list
        """
        try:
            list3=[]
            for i in range(d):
                list3.append(0)
            return list3
        except Exception as e:
            raise e 
    def intialize_passengers(self,d):
        """
        It takes number of vechiles as argument and return a list where no of passengers in each vechile is intialized to 0
        Args:
            d (int):vechiles number

        Returns:
            list
        """
        try:
            list3=[]
            for i in range(d):
                list3.append(0)
            return list3
        except Exception as e:
            raise  e 
    def intialize_vechile_list(self):
        """
          return a list of lists of size equal to no of vechiles
        Returns:
            list of lists
        """
        try:
            list3=[]
            for i in range(self.d):
                list3.append([])
            return list3
        except Exception as e:
            raise  e 
    def intialize_vechile_distance(self,d):
        """
        It takes number of vechiles as argument and return a list where vechile travel distance is equal to 0
        Args:
            d (int):vechiles number

        Returns:
            list
        """
        try:
            list3=[]
            for i in range(d):
                list3.append(0)
            return list3
        except Exception as e:
            raise e 
    def intialize_vechile_travelled(self):
        """
        It takes number of vechiles as argument and return a list where vechile travel distance is equal to 0
        Args:
            d (int):vechiles number

        Returns:
            list
        """
        try:
            list3=[0]
            list4=[]
            for i in range(self.d):
                list4.append([0])
            return list4
        except Exception as e:
            raise e
        
    def average_distance(self):
        """ 
        This function return average_distance travelled by a car 
        """
        try:
            sum=0
            for i in range(self.d):
                sum=sum+self.vechile_travel_distance[i]
            return sum/self.d
        except Exception as e:
            raise e
    def average_trips(self):
        """
        This function returns average no of trips travelled
        Returns:
            int
        """
        try:
            return self.no_of_trips/self.f
        except Exception as e:
            raise e                            
    def __init__(self):
        a=1000
        self.b=10
        self.d=2
        self.e=5
        self.f=20
        self.no_of_trips=0
        self.count=1
        self.cus_dir={}
        self.pick_up_requests=1
        self.cust_list=[[8,9],[3,6],[4,7],[2,4],[1,7],[1,9]]
        self.vechile_list=self.intialize_vechile_list()
        self.vechile_travelled=self.intialize_vechile_travelled()
        self.vechile_track=self.intialize_vechile_track()
        self.curr_vechile_location=self.intialize_curr_location(self.d)
        self.no_of_passengers=self.intialize_passengers(self.d)
        self.vechile_travel_distance=self.intialize_vechile_distance(self.d)
        self.G=self.generate_connected_graph(a,self.b,self.d,self.e,self.f)
        weights=None
        self.G=self.Add_weights_to_graph(weights,self.G)
        self.clock_ticks=1
        while self.clock_ticks<self.f:
            print("vechile 1 queue:",self.vechile_list[0])
            print("")
            print("vechile 2 queue:",self.vechile_list[1])
            print("")
            print("curr",self.curr_vechile_location[0])
            print("")
            print("curr",self.curr_vechile_location[1]) 
            print("nodes travelled by vechile 1:",self.vechile_travelled[0])
            print("")
            print("nodes travelled by vechile 2:",self.vechile_travelled[1])
            print("")
            print("")
            if self.clock_ticks<=3:
                self.TakeRideRequests(self.G)
                self.pick_customers()
                self.drop_customers()
                self.pick_up_requests=self.pick_up_requests+1
                self.clock_ticks=self.clock_ticks+1
            else:
                print(self.clock_ticks)
                if self.clock_ticks==19:
                    print(len(self.vechile_list[0]))
                    print(len(self.vechile_list[1]))
                    
                self.update()
                self.pick_customers()
                self.drop_customers()
                self.clock_ticks=self.clock_ticks+1
        flag=0
        while flag==0:
            flag=1
            for i in range(self.d):
                if len(self.vechile_list[i])>0:
                    flag=0
            if flag==0:
                print("vechile 1 queue:",self.vechile_list[0])
                print("")
                print("vechile 2 queue:",self.vechile_list[1])
                print("")
                print("curr",self.curr_vechile_location[0])
                print("")
                print("curr",self.curr_vechile_location[1]) 
                print("nodes travelled by vechile 1:",self.vechile_travelled[0])
                print("")
                print("nodes travelled by vechile 2:",self.vechile_travelled[1])
                print("")
                print("")
                self.clock_ticks=self.clock_ticks+1
                self.update()
                self.pick_customers()
                self.drop_customers()
                
        """for i in self.cus_dir:
            print(self.cus_dir[i][0]," ",self.cus_dir[i][1]," ",self.cus_dir[i][2]," ",self.cus_dir[i][3]," ",self.cus_dir[i][4])"""


x=uber()