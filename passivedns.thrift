#!/usr/local/bin/thrift -py

struct dns_record {
  1: string key,
  2: string value,
  3: string type = 'A',
  4: i32 ttl = 86400,
  5: string first,
  6: string last
}

typedef list<dns_record> biglist

struct dns_response {
    1: biglist records
}

service PassiveDns {
   biglist search_question(1:string q);
   biglist search_answer(1:string q);
}
