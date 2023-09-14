def octet_split(x):
    ip_address = x

    octets = ip_address.split('.')
    octet1, octet2, octet3, octet4 = octets
    return octet1, octet2, octet3, octet4

def bi_octet_split(x):
    ip_address = x

    octet1=ip_address[0:8]
    octet2=ip_address[8:16]
    octet3=ip_address[16:24]
    octet4=ip_address[24:]
    return octet1, octet2, octet3, octet4


oc1,oc2,oc3,oc4 = bi_octet_split("11000000101010001111111110000000")

print(f" {oc1}  , {oc2} , {oc3} , {oc4}")

def ip_conv_bin_dic(x): 
    oc1,oc2,oc3,oc4 = bi_octet_split(x)
    ipaddr=f"{int(oc1, base=2)}.{int(oc2, base=2)}.{int(oc3, base=2)}.{int(oc4, base=2)}"
    return ipaddr


print(ip_conv_bin_dic("11000000101010001111111100000000"))










