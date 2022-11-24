import compile_protos.get_data_entry_pb2_grpc
import compile_protos.get_data_entry_pb2

import time
import grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        # console.log("🚀 ~ file: get_data_client.py ~ line 10 ~ localhost", localhost)
        stub = get_data_entry_pb2_grpc.DataEntryGetterStub(channel)
        get_data_entry_request = get_data_entry_pb2.GetDataEntryRequest(
            dataset_id="637cc07f1ba9ee2e6b7e2ed3"
        )
        get_data_entry_reply = stub.GetDataEntry(get_data_entry_request)
        print(get_data_entry_reply)


if __name__ == "__main__":
    run()
