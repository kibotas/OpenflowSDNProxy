#include <bcc/proto.h>
#include <openflow.h>
#include <net/sock.h>

#define ETH_HLEN sizeof(struct ethernet_t)
#define IP_HLEN sizeof(struct ip_t)
#define TCP_HLEN sizeof(struct tcp_t)
#define OFP_HLEN sizeof(struct ofp_header)
#define DROP 0
#define PASS -1

int openflowfilter(struct __sk_buff *skb)
{
    u8 *cursor = 0;
    // cursor_advance returns the value of cursor pointer and moves the pointer forward 'second argument' many bytes
    // for more informations see https://stackoverflow.com/questions/60249948/what-exactly-is-usage-of-cursor-advance-in-bpf
    struct ethernet_t *ethernet = cursor_advance(cursor, sizeof(*ethernet));
    struct ip_t *ip;
    struct tcp_t *tcp;

    // Only allow IP packets to enter (ethernet type = 0x0800)
    if (!(ethernet->type == 0x0800)) {
	return DROP;
    }

    ip = cursor;

    if(!(ip->nextp==6)){
        bpf_trace_printk("No TCP, instead %u", ip->nextp);
        return DROP;
    }

    // Advance the cursor ip_len ( variable ) bytes
    u8 ip_len = ip->hlen <<2;
    ip = cursor_advance(cursor, ip_len);

    tcp = cursor;

    // Assess the correct TCP port
    if(tcp->dst_port==6653)
        return PASS;

    return DROP;
}



/*
    //bpf_trace_printk("SRC PORT %u DST PORT %u", tcp->src_port, tcp->dst_port);
    u8 src = tcp->src_port;
    u8 dst = tcp->dst_port;

    u8 tcp_len = tcp->offset<<2; 
    //bpf_trace_printk("TCP LENGTH %u", tcp_len);

    // offset * 4 Byte = tcp header length
    u8 data_len = ip->tlen - ip_len - tcp_len;
    //bpf_trace_printk("Data len %u", data_len);

    if(data_len >= sizeof(struct ofp_header)){
        bpf_trace_printk("Maybe Openflow %u", data_len);
        return PASS;
    }
    return DROP;
    //bpf_trace_printk("Too short %u", data_len);

    return DROP;

    /*struct ofp_header *ofp = cursor_advance(cursor, tcp_len);

    u8 version1;
    u8 version2;
    u8 result = bpf_probe_read_kernel(&version1, sizeof(version1), ofp);
    result = bpf_probe_read_kernel(&version2, sizeof(version1), ofp+1);
    bpf_trace_printk("Version %x", version1);
    bpf_trace_printk("Version %x", version2);
    //struct ofp_header *ofp_h;
    //if(result != 0)
        //return DROP;

    struct ofp_header ofp_h;
    //u8 result = bpf_probe_read_kernel(&ofp_h, sizeof(ofp_h), &ofp);
    //bpf_trace_printk("Version %x", ofp_h.version);
    //bpf_trace_printk("Type %x", ofp_h.type);
    //bpf_trace_printk("Length %x", ofp_h.length);
    //bpf_trace_printk("XID %x", ofp_h.xid);
    //bpf_trace_printk("Version %u", ofp_h->version);
    //if(version!=0x06){
    //    return DROP;
   // }
}
   */
