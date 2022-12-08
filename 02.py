import sys
import time
from mininet.log import info, setLogLevel
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
import io 
import contextlib


def topology(args):

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    h1 = net.addHost( 'h1', mac='AA-7F-79-34-99-9D', ip='10.0.0.1/8' )
    sta1 = net.addStation( 'sta1', mac='AA-7F-79-34-99-9G', ip='10.0.0.2/8', range='5' )
    ap1 = net.addAccessPoint( 'ap1', ssid= 'ap1-ssid', mode= 'g', channel= '1', position='100,100,0', range='80' )
    c1 = net.addController( 'c1' )

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, h1)
    if '-p' not in args:
        net.plotGraph(max_x=200, max_y=160)

    net.setMobilityModel(time=0, model='RandomDirection', max_x=200, max_y=200, seed=10)
    
    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    cont=1
    distan=[]
    d=-1
    if '-V'  in args:
        while cont!=25:
            time.sleep(2.4)
            x= sta1.get_distance_to(ap1)
            distan.append(x)
            d=d+1
            if len(distan)>1 :   
                print("\nDistancia : ",x)
        
            if len(distan) >1 and (distan[d-1]<distan[d]) and (distan[d]<80.0):
                nodes=net.switches+net.hosts
                for node in nodes:
                    #print(node)
                    for intf in node.intfList(): 
            
                        if intf.link:
                            newBW = 5+cont
                            intfs = [ intf.link.intf1, intf.link.intf2 ] 
                            intfs[0].config(bw=newBW) 
                            intfs[1].config(bw=newBW)
                            print("\n")
                            # break;
                        else:
                                print("erro")
            cont=cont+1;
            


    CLI( net )

  
    info("*** Stopping network\n")
    net.stop()
if __name__ == '__main__':
    setLogLevel( 'info' )
    topology(sys.argv)