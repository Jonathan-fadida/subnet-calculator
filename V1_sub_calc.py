import re
import math

def octet_split(x: str) -> list :
    '''
    Splits an IPv4 address string into octets and returns a list of octets.
    '''

    octets = x.split('.')
    return octets


def conv_ipv4_32bit(ipv4_add):    
    '''
    Converts an IPv4 address to a 32-bit binary representation.
    '''
    list_ip=ipv4_add.split(".")
    ipv4_bits=0
    for octet in list_ip:
        octet_int = int(octet)
        ipv4_bits = (ipv4_bits << 8) | octet_int

    return bin(ipv4_bits).replace('0b','')
    

def bits_split(x):
    '''
    Splits a 32-bit binary string into 4 octets and returns them.
    '''
    bits = x
    octet1=bits[0:8]
    octet2=bits[8:16]
    octet3=bits[16:24]
    octet4=bits[24:]
    return  octet1, octet2, octet3, octet4 


def conv_32bit_ipv4(x): 
    '''
    Converts a 32-bit binary string to an IPv4 address.
    '''
    oc1,oc2,oc3,oc4 = bits_split(x)
    ip_addr=f"{int(oc1, base=2)}.{int(oc2, base=2)}.{int(oc3, base=2)}.{int(oc4, base=2)}"
    return ip_addr


def prompt_ip():

    '''
    Prompts the user to enter an IPv4 address and returns the address along with its class and default CIDR.
    '''

    p = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
   
    while True:
        my_ip=input("please enter ip address here: ")

        if re.match(p, my_ip):
        
            first_octet = int(my_ip.split('.')[0])

            if 1 <= first_octet <= 126:
                ip_class = 'A'
                default_cidr = 8
            elif 128 <= first_octet <= 191:
                ip_class = 'B'
                default_cidr = 16
            elif 192 <= first_octet <= 223:
                ip_class = 'C'
                default_cidr = 24
            elif 224 <= first_octet <= 239:
                ip_class = 'D'
                default_cidr = None  
            else:
                ip_class = 'E'
                default_cidr = None  

            
            return my_ip, ip_class  ,default_cidr
        
        else :
            print("Please enter a valid IP Address")


def prompt_CIDR(dif_cidr):
    '''
    Prompts the user to enter a CIDR notation or leave it empty and returns the CIDR.
    '''
    while True:
        try:
            CIDR_input = input("type CIDR or leave Empty(press Enter) : ")
            if not CIDR_input and not dif_cidr:
                print("you can't skip you should provide a valid CIDR ")
                print("because you brovided an Ip address of class E or D")
                continue
            if not CIDR_input :
                cidr=dif_cidr
                return cidr


            cidr=int(CIDR_input)

            if 0 <= cidr <= 32 : 
                return cidr
                #break
            else :
                print("Enter valid cidr shorthand")    

        except ValueError:
            print("Enter valid cidr shorthand")   



def prompt_chooice(cidr):
    '''
    Prompts the user to choose between calculating based on hosts or subnets and returns the choice along with the number of hosts/subnets.
    '''
    available_addresses = 2 ** (32 - cidr)
    
    while True:
        choice = input("Choose how your calculation depends on hosts or subnets: ")
        if choice.lower() in ['hosts', 'subnets']:
            choice = choice.lower()
            break
        else:
            print("Invalid input. Please enter 'hosts' or 'subnets.")

    while True:
        amount = input("Enter the amount of hosts/subnets: ")
        if amount.isdigit():
            amount = int(amount)
            if choice == "hosts":
                curr_addresses = 2 ** (math.ceil(math.log2(amount+2)))
                if curr_addresses > available_addresses:
                    print(f"your network can't have {curr_addresses} addresses")
                    print(f"note: your network can have maximum of {available_addresses} addresses")

                    continue
                elif curr_addresses == available_addresses:
                    print(f"If you want to have {amount} hosts, you will remain with one network.")
                    flag = input("Type 'y' to continue or 'n' to modify the amount: ")
                    if flag.lower() == "y":
                        return choice, amount
                
                
                    
                else:
                    return choice, amount
            elif choice == "subnets":
                curr_addresses = 2 ** (math.ceil(math.log2(amount)))
                if curr_addresses > available_addresses:
                    print(f"your network can't have {curr_addresses} addresses")
                    print(f"note: your network can have maximum of {available_addresses} addresses")
                    continue
                        
                elif curr_addresses == available_addresses:
                    print("if you choose this amount of subnets you will have no availbe Ips in your subnets ")
                    flag = input("Type 'y' to continue or 'n' to modify the amount: ")
                    if flag.lower() == "y":
                        return choice, amount
                
                else :
                    return choice, amount
        else:
            print("Invalid input. Please enter a valid amount.")




def conv_cidr_mask(cidr):  
    '''
    Converts a CIDR notation to a subnet mask.
    '''    
    bits_cidr = "1" * cidr + "0" * (32 - cidr)
    mask = conv_32bit_ipv4(bits_cidr)
    return mask
 



   
def calc_bits_subnets_and_hosts(choice,amount,cidr):
    '''
    Calculates the number of bits for subnets and hosts based on the user's choice and input.
    '''    
    if choice == "subnets":
        bits_for_subnets = math.ceil(math.log2(amount))
        bits_for_hosts = 32 - cidr - bits_for_subnets
    else :
        bits_for_hosts = math.ceil(math.log2(amount+2))
        bits_for_subnets = 32 - cidr - bits_for_hosts

    return bits_for_subnets , bits_for_hosts



def calc_2_first_last_subs(ip,cidr,bits_hosts):
    '''
    Calculates the first and last subnets, as well as their broadcast addresses, based on the input IP, CIDR, and number of bits for hosts.
    '''  
    
    hosts=2**bits_hosts
    
    subnets_cidr=32-bits_hosts

    bits_ip=conv_ipv4_32bit(ip)
    
    

    first_subnet=f"{ip}/{subnets_cidr}"
    int_first_broadcast=int(bits_ip,2) | (hosts-1)
    first_broadcast=conv_32bit_ipv4(bin(int_first_broadcast).replace('0b','').zfill(32))

    int_second_ip=int(bits_ip,2) | hosts
    second_ip=conv_32bit_ipv4(bin(int_second_ip).replace('0b','').zfill(32))
    int_second_broadcast=int(bits_ip,2) | (hosts+hosts-1)
    second_broadcast=conv_32bit_ipv4(bin(int_second_broadcast).replace('0b','').zfill(32))
    second_subnet=f"{second_ip}/{subnets_cidr}"



    int_third_ip=int(bits_ip,2) | ((2**(32-cidr))-hosts)
    third_ip=conv_32bit_ipv4(bin(int_third_ip).replace('0b','').zfill(32))
    int_third_broadcast=int(bits_ip,2) | ((2**(32-cidr))-1)
    third_broadcast=conv_32bit_ipv4(bin(int_third_broadcast).replace('0b','').zfill(32))
    third_subnet=f"{third_ip}/{subnets_cidr}"


    int_fourth_ip=int(bits_ip,2) | (2**(32-cidr)-(hosts*2))
    fourth_ip=conv_32bit_ipv4(bin(int_fourth_ip).replace('0b','').zfill(32))
    int_fourth_broadcast=int(bits_ip,2) | ((2**(32-cidr))-hosts-1)
    fourth_broadcast=conv_32bit_ipv4(bin(int_fourth_broadcast).replace('0b','').zfill(32))
    fourth_subnet=f"{fourth_ip}/{subnets_cidr}"
    

    if subnets_cidr == 32:
        print(f"subnet1){first_subnet} , subnet2) {second_subnet} ")
        print(f"subnet3) {third_subnet} , subnet4) {fourth_subnet}")
        #return first_subnet , second_subnet , third_subnet , fourth_subnet
    elif subnets_cidr == cidr+1:
        print(f" first subnet:{first_subnet} , first broadcast: {first_broadcast} ")
        print(f"second subnet {second_subnet} , second broadcast: {second_broadcast} ")
    elif subnets_cidr == cidr:
        print(f"Network:{first_subnet} , Broadcast:{first_broadcast}") 

    else:
        print(f"first subnet:{first_subnet} , first_broadcast:{first_broadcast}") 
        print(f"second subnet:{second_subnet} , second_broadcast:{second_broadcast}")
        print(f"second last subnet:{fourth_subnet} , second last broadcast:{fourth_broadcast}")
        print(f"last subnet:{third_subnet} , last broadcast:{third_broadcast}")



def main():
    my_ip , my_class , my_dif_cidr =  prompt_ip()
    cidr=prompt_CIDR(my_dif_cidr)
    mask_cidr=conv_cidr_mask(cidr)
    choice , amount = prompt_chooice(cidr)
    bits_subnets , bits_hosts = calc_bits_subnets_and_hosts(choice,amount,cidr)
    #fff  =(calc_2_first_last_subs(my_ip,cidr,bits_hosts))


    # print(my_ip , my_class , my_dif_cidr)
    # print(choice, amount)
    # print(f"subs--{2**bits_subnets}--  hosts --{2**bits_hosts}")
    # print(f" fff {fff} ")

    print(mask_cidr)
    print(cidr)
    print(f"Subnets : {2**bits_subnets} -- hosts --{(2**bits_hosts) -2 }")
    calc_2_first_last_subs(my_ip,cidr,bits_hosts)
main()


