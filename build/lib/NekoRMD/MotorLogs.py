

class MotorLogs:
    def decode_motor_message(self, request):
        pass

    def decode_motor_response(self, response):
        if response:
            data = response.data
            print(f"Response ID: {response.arbitration_id}")
            print(f"Response Data: {[hex(b) for b in data]}")
            if data[0] == 0xA1:
                iq_current = data[1] | (data[2] << 8)
                iq_current = iq_current if iq_current < 32768 else iq_current - 65536  # convert to signed
                print(f"Torque Current Response: {iq_current} mA")
            else:
                print("Unexpected response")
        else:
            print("No response received")