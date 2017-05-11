import struct

messageVal = 0.40

message_bytes = [];
message_bytes.append(0xDE)
message_bytes.append(0xAD)

ba1 = bytearray(struct.pack("f", 0.00))
ba2 = bytearray(struct.pack("f", 0.40))
ba3 = bytearray(struct.pack("f", -0.40))
ba4 = bytearray(struct.pack("f", 0.99))
ba5 = bytearray(struct.pack("f", -1.00))

message_bytes += ba1
message_bytes += ba2
message_bytes += ba3
message_bytes += ba4
message_bytes += ba5

message_bytes.append(0xBE)
message_bytes.append(0xEF)


for b in message_bytes:
	print hex(b),
print len(message_bytes)