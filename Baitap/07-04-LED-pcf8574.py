import smbus
from time import sleep

# ĐIỀU KHIỂN MÀN HÌNH LCD QUA CHIP MỞ RỘNG PCF8574 (GIAO TIẾP I2C)

class PCF8574_LCD:
    def __init__(self, address, bus_num=1):
        """
        Hàm khởi tạo cấu hình cho màn hình LCD
        address: Địa chỉ I2C của module PCF8574 (thường là 0x27 hoặc 0x3f)
        bus_num: Cổng I2C bus trên Pi (mặc định là cổng 1)
        """
        self.address = address
        self.bus = smbus.SMBus(bus_num)
        
        # Định nghĩa các Bit mặt nạ (Bitmask) tương ứng với các chân nối từ PCF8574 sang LCD:
        self.MASK_RS = 0x01       # Chân P0 của chip: Chọn thanh ghi (0 = Gửi Lệnh, 1 = Gửi Chữ)
        self.MASK_RW = 0x02       # Chân P1 của chip: Đọc/Ghi dữ liệu (0 = Ghi, 1 = Đọc)
        self.MASK_E  = 0x04       # Chân P2 của chip: Chân Kích hoạt (Enable), dùng để chốt dữ liệu
        self.MASK_BL = 0x08       # Chân P3 của chip: Điều khiển Bật/Tắt đèn nền (Backlight) của màn hình
        
        # -----------------------------------------------------------------
        # QUY TRÌNH KHỞI TẠO MÀN HÌNH THEO CHUẨN MÃ HD44780 (CHẾ ĐỘ 4-BIT)
        # -----------------------------------------------------------------
        # Chế độ 4-bit giúp tiết kiệm chân, nhưng lúc khởi tạo phải gửi lệnh mồi 0x03 ba lần
        sleep(0.05)
        self._write_cmd_4bit(0x03) # Lần mồi 1
        sleep(0.005)
        self._write_cmd_4bit(0x03) # Lần mồi 2
        sleep(0.001)
        self._write_cmd_4bit(0x03) # Lần mồi 3
        
        self._write_cmd_4bit(0x02) # Lệnh chính thức chuyển màn hình sang chế độ giao tiếp 4-bit
        
        # Thiết lập các thông số hiển thị cơ bản:
        self.write_cmd(0x28) # Lệnh 0x28: Chọn chế độ 4-bit, màn hình có 2 dòng, phông chữ 5x8 pixel
        self.write_cmd(0x0C) # Lệnh 0x0C: Bật màn hình lên, đồng thời TẮT con trỏ nhấp nháy (cho đỡ ngứa mắt)
        self.clear()         # Xóa sạch màn hình về trạng thái trống ban đầu

    def _write_pcf8574(self, data):
        """ Hàm ghi 1 byte dữ liệu thô trực tiếp ra chip PCF8574 qua sóng I2C """
        # Ta dùng phép toán OR (|) với MASK_BL để đảm bảo đèn nền luôn luôn BẬT trong mọi lượt gửi dữ liệu
        self.bus.write_byte(self.address, data | self.MASK_BL)

    def _pulse_enable(self, data):
        """ Tạo một xung kích hoạt (Kéo chân Enable lên Cao rồi hạ xuống Thấp) để LCD chốt dữ liệu """
        self._write_pcf8574(data | self.MASK_E)  # Kéo chân E lên 1 (HIGH) để mở cổng nhận
        sleep(0.0005)                            # Đợi một chút siêu ngắn (0.5 mili giây) để dữ liệu ổn định
        self._write_pcf8574(data & ~self.MASK_E) # Hạ chân E về 0 (LOW) để khóa cổng, hoàn thành chốt dữ liệu
        sleep(0.0005)                            # Đợi màn hình xử lý xong trước khi làm việc tiếp

    def _write_cmd_4bit(self, value):
        """ Hàm phụ trợ dùng riêng để gửi các lệnh mồi 4-bit lúc vừa bật nguồn """
        data = (value << 4) & 0xF0 # Dịch giá trị sang trái 4 bit để đưa vào 4 chân dữ liệu cao (P4-P7)
        self._write_pcf8574(data)  # Ghi dữ liệu thô ra chip
        self._pulse_enable(data)   # Gõ lệnh chốt chân Enable

    def write_byte(self, value, mode):
        """ 
        HÀM CỐT LÕI: Gửi trọn vẹn 1 byte (8-bit) dữ liệu sang màn hình LCD.
        Vì đang chạy chế độ 4-bit, ta phải xẻ đôi byte này ra: Gửi 4 bit cao trước, 4 bit thấp sau.
        mode: Điền self.MASK_RS nếu gửi Ký tự chữ, điền 0 nếu gửi câu Lệnh cấu hình.
        """
        # LƯỢT 1: Trích xuất 4 bit cao (High Nibble)
        # (value & 0xF0) giữ nguyên 4 bit đầu và xóa 4 bit sau. Sau đó kết hợp với mode (RS) bằng phép OR (|)
        hi_nibble = (value & 0xF0) | mode
        
        # LƯỢT 2: Trích xuất 4 bit thấp (Low Nibble)
        # Dịch trái 4 bit (value << 4) để đẩy 4 bit thấp lên vị trí cao, rồi lọc lại bằng & 0xF0 và kết hợp với mode
        lo_nibble = ((value << 4) & 0xF0) | mode
        
        # Thực hiện gửi lượt 1 (4 bit cao) và ra lệnh chốt
        self._write_pcf8574(hi_nibble)
        self._pulse_enable(hi_nibble)
        
        # Thực hiện gửi lượt 2 (4 bit thấp) và ra lệnh chốt
        self._write_pcf8574(lo_nibble)
        self._pulse_enable(lo_nibble)

    def write_cmd(self, cmd):
        """ Hàm dùng để gửi một câu lệnh cấu hình hệ thống (gọi write_byte với mode = 0) """
        self.write_byte(cmd, 0)

    def clear(self):
        """ Hàm xóa toàn bộ nội dung hiển thị trên màn hình """
        self.write_cmd(0x01) # Mã lệnh 0x01 trong datasheet quy định việc xóa sạch màn hình
        sleep(0.002)         # Lệnh xóa tốn thời gian xóa bộ nhớ, cần sleep 2ms để LCD kịp xử lý

    def move_to(self, row, col):
        """ 
        Hàm di chuyển con trỏ hiển thị đến vị trí mong muốn
        row: Dòng muốn viết (0 là dòng trên, 1 là dòng dưới)
        col: Cột muốn viết (Từ cột 0 đến cột 15)
        """
        # Datasheet quy định: Địa chỉ gốc dòng 1 bắt đầu từ 0x80, dòng 2 bắt đầu từ 0xC0
        base_addr = 0x80 if row == 0 else 0xC0
        final_addr = base_addr + col # Cộng thêm số cột để ra vị trí chính xác
        self.write_cmd(final_addr)   # Gửi lệnh nhảy con trỏ sang LCD

    def write_string(self, message):
        """ Hàm nhận vào một chuỗi chữ (String) và duyệt in từng ký tự ra màn hình """
        for char in message:
            # ord(char) dùng để lấy mã số ASCII (1 byte) của ký tự đó (Ví dụ: ord('A') -> 65)
            # Truyền kèm self.MASK_RS để thông báo cho LCD biết đây là dữ liệu CHỮ chứ không phải lệnh
            self.write_byte(ord(char), self.MASK_RS)


# =========================================================================
# HÀM ĐỌC CẢM BIẾN NHIỆT ĐỘ I2C ADT7410 
# =========================================================================
def read_adt7410():
    """ Hàm đọc dữ liệu thô từ cảm biến ADT7410 (địa chỉ 0x48) và quy đổi sang độ C """
    # Bước 1: Gửi lệnh I2C đọc 2 byte dữ liệu liên tiếp (Word Data) bắt đầu từ thanh ghi 0x00
    word_data = bus.read_word_data(0x48, 0x00)
    
    # Bước 2: Đảo byte (Byte Swap)
    # Vì chip ADT7410 gửi Byte cao trước, Byte thấp sau (Big-Endian), nhưng Raspberry Pi 
    # lại đọc theo kiểu ngược lại (Little-Endian). Ta phải dùng toán tử dịch bit để tráo đổi vị trí của chúng.
    data = (word_data & 0xff00) >> 8 | (word_data & 0xff) << 8
    
    # Bước 3: Con chip này chỉ lưu giá trị nhiệt độ ở 13 bit đầu tiên trong tổng số 16 bit trả về.
    # 3 bit cuối cùng là các bit cờ trạng thái (Flags). Ta dịch phải 3 bit (>> 3) để vứt bỏ 3 bit rác này đi.
    data = data >> 3 
    
    # Bước 4: Kiểm tra xem nhiệt độ là số Dương hay số Âm
    # Ta kiểm tra bit dấu (bit thứ 13, tương ứng với mặt nạ mã Hex là 0x1000)
    if data & 0x1000 == 0: 
        # Nếu bit dấu bằng 0 -> Nhiệt độ Dương (hoặc bằng 0)
        # Datasheet quy định mỗi đơn vị số tương ứng với biến thiên 0.0625 độ C
        temperature = data * 0.0625
    else: 
        # Nếu bit dấu bằng 1 -> Nhiệt độ Âm. Phải làm phép toán lấy mã bù 2 (Two's Complement)
        # Đảo ngược toàn bộ bit (~data), lọc lấy 13 bit (& 0x1fff), cộng thêm 1 rồi nhân với số âm
        temperature = ((~data & 0x1fff) + 1) * -0.0625
        
    return temperature


# =========================================================================
# KHỐI THỰC THI CHƯƠNG TRÌNH CHÍNH (MAIN PROGRAM)
# =========================================================================
if __name__ == '__main__':
    # Khởi tạo đối tượng quản lý giao tiếp I2C bus số 1 của mạch Pi
    bus = smbus.SMBus(1)
    
    # Khai báo địa chỉ quét được từ lệnh i2cdetect của module LCD (mặc định đa số là 0x27)
    LCD_ADDR = 0x27 
    
    try:
        # Khởi tạo màn hình LCD với địa chỉ cấu hình ở trên
        lcd = PCF8574_LCD(LCD_ADDR)
        
        # Thiết lập giao diện tĩnh cố định (Chỉ cần viết 1 lần duy nhất, không bỏ vào vòng lặp)
        lcd.move_to(0, 0)               # Di chuyển về hàng 0, cột 0
        lcd.write_string("Phenikaa IT") # In tên khoa/trường của bạn làm thương hiệu thương mại
        
        lcd.move_to(1, 0)               # Di chuyển xuống hàng 1, cột 0
        lcd.write_string("Temp:")       # In nhãn chữ "Temp:" cố định
        
        print("Hệ thống hiển thị nhiệt độ đang chạy mượt mà... Bấm Ctrl + C để dừng.")
        
        # Vòng lặp quét dữ liệu liên tục thời gian thực
        while True:
            # 1. Gọi hàm lấy giá trị nhiệt độ phòng từ cảm biến ADT7410
            inputValue = read_adt7410()
            
            # 2. Đẩy dữ liệu lên màn hình LCD (Bọc trong khối try...except chống sập mạch)
            try:
                # Chỉ định vị trí bắt đầu in con số nhiệt độ biến thiên (Hàng 1, cột số 6, ngay sau chữ Temp:)
                lcd.move_to(1, 6)
                
                # Biến đổi số thực sang chuỗi String và định dạng đẹp mắt lấy đúng 2 chữ số sau dấu phẩy.
                # Chuỗi kết quả sẽ có dạng như: "26.34 C"
                temp_str = f"{inputValue:.2f} C"
                
                # Gửi chuỗi ký tự sạch này sang cho LCD hiển thị
                lcd.write_string(temp_str)
                
            except IOError:
                # Nếu chẳng may đường dây nhảy bị lỏng trong tích tắc, Pi sẽ bắt được lỗi này,
                # in thông báo ra màn hình máy tính và bỏ qua lượt quét này chứ không làm sập toàn bộ hệ thống.
                print("[Cảnh báo] Lỗi nhiễu tín hiệu đường truyền I2C. Đang bỏ qua lượt này...")
            
            # Nghỉ ngơi 1 giây trước khi vào chu kỳ quét tiếp theo
            sleep(1.0)
            
    except KeyboardInterrupt:
        # Bẫy lệnh ngắt khi người dùng bấm nút Stop đỏ trong Thonny hoặc gõ Ctrl + C trên Terminal
        print("\n[Thông báo] Đang tiến hành dọn dẹp hệ thống nhúng...")
        lcd.clear() # Xóa sạch chữ trên màn hình để tiết kiệm điện năng và bảo vệ điểm ảnh cho LCD
        print("Đã tắt màn hình an toàn.")