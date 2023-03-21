# connecting-sdn-slices
Networking 2 project

## Demo
### Setting up the network
Start up and log into the VM:<br>
```vagrant up comnetsemu```<br>
```vagrant ssh comnetsemu```<br>

Run the script to enable the RYU controllers to load the application:<br>
```./runcontrollers.sh```<br>

In an other terminal, start the network with mininet:<br>
```$ sudo python3 network.py```<br>

pingall

### Intra-slice communication (Hosts in the same slice)
Host 8 can send TCP packets to Host 3:<br>
```h3 iperf -s &```<br>
```h8 iperf -c 10.0.0.3 -t 10 -i 1```<br>

Host 1 can send UDP packets to Host 5<br>
```h5 iperf -s -u &```<br>
```h1 iperf -c 10.0.0.5 -u -t 10 -i 1```<br>

### Inter-slice communication (Hosts in different slices)
Host 2 (slice 1) can send TCP packets to Host 3 (slice 2) on port 3000:<br>
```h3 iperf -s -p 3000 &```<br>
```h2 iperf -c 10.0.0.3 -p 3000 -t 10 -i 1```<br>

Host 1 (slice 1) can send TCP packets to Host 10 (slice 3) regardless of the port chosen:<br>
```h10 iperf -s &```<br>
```h1 iperf -c 10.0.0.10 -t 10 -i 1```<br>

Host 4 (slice 2) cannot send TCP packets to Host 6 (slice 1) on a different port:<br>
```h4 iperf -s -p 4000 &```<br>
```h6 iperf -c 10.0.0.4 -p 4000 -t 10 -i 1```<br>

Host 2 (slice 1) cannot send UDP packets to Host 7 (slice 2):<br>
```h7 iperf -s -u &```<br>
```h2 iperf -c 10.0.0.7 -u -t 10 -i 1```<br>

Flow table for switch 12 (connecting slice):<br>
```$ sudo ovs-ofctl dump-flows s12```<br>

