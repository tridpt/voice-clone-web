"""Bộ câu mẫu tiếng Việt để đọc khi thu âm dữ liệu huấn luyện.

Các câu được chọn để phủ đa dạng:
- Đủ 6 thanh điệu (ngang, huyền, sắc, hỏi, ngã, nặng)
- Nhiều phụ âm đầu/cuối và nguyên âm khác nhau
- Có câu chứa số, ngày tháng, câu hỏi, câu cảm thán để giọng tự nhiên
- Có vài từ khó phát âm để model học chắc hơn
- Độ dài vừa phải (2–15 giây khi đọc), hợp để cắt thành mẫu train

Khuyến nghị: thu ít nhất 80–100 câu (~10–20 phút) để fine-tune cho
chất lượng tốt. Thu càng nhiều, giọng clone càng giống và tự nhiên.
"""

SAMPLE_SENTENCES = [
    # --- Câu chào, giới thiệu ---
    "Xin chào, đây là giọng nói mẫu của tôi dùng để huấn luyện mô hình.",
    "Rất vui được gặp bạn, tôi tên là An, hiện đang sống ở Hà Nội.",
    "Cảm ơn bạn đã lắng nghe, chúc bạn một ngày thật nhiều niềm vui!",
    "Tôi rất thích đọc sách, nghe nhạc và viết lách vào những ngày cuối tuần.",
    "Năm nay tôi hai mươi lăm tuổi, đang làm việc tại một công ty công nghệ.",

    # --- Thiên nhiên, thời tiết ---
    "Hôm nay trời nắng đẹp, tôi đi dạo quanh hồ vào buổi sáng sớm.",
    "Mùa thu Hà Nội đẹp lạ lùng với những hàng cây thay lá vàng rực.",
    "Dòng sông quê hương hiền hòa chảy qua bao mùa mưa nắng.",
    "Gió biển thổi mát rượi, từng con sóng vỗ nhẹ vào bờ cát trắng.",
    "Bầu trời đêm nay đầy sao, ánh trăng soi sáng cả khu vườn yên tĩnh.",
    "Cơn mưa rào bất chợt khiến đường phố ngập tràn tiếng cười trẻ thơ.",
    "Sương sớm còn đọng trên lá, không khí trong lành đến lạ.",
    "Những ngọn núi trùng điệp ẩn hiện sau làn mây trắng bồng bềnh.",
    "Tiếng chim hót líu lo báo hiệu một ngày mới bắt đầu.",
    "Cánh đồng lúa chín vàng óng trải dài tới tận chân trời.",

    # --- Sinh hoạt thường ngày ---
    "Con mèo nhỏ nằm cuộn tròn ngủ ngon lành bên cạnh lò sưởi ấm áp.",
    "Chú chó vẫy đuôi mừng rỡ khi thấy chủ trở về sau một ngày dài.",
    "Mẹ dặn tôi nhớ mặc áo ấm vì ngoài trời đang trở lạnh dần.",
    "Bà kể chuyện cổ tích cho cháu nghe mỗi tối trước khi đi ngủ.",
    "Buổi sáng tôi thường uống một tách cà phê nóng và đọc tin tức.",
    "Chiếc xe màu đỏ chạy bon bon trên con đường làng yên ả.",
    "Anh ấy chạy thật nhanh để kịp chuyến tàu lúc bảy giờ sáng.",
    "Cẩn thận nhé, sàn nhà vừa lau xong nên còn hơi trơn đấy!",
    "Tôi quên mang ô nên bị ướt sũng cả người khi tan làm.",
    "Cả nhà quây quần bên mâm cơm tối ấm cúng và rôm rả chuyện trò.",

    # --- Ẩm thực ---
    "Ôi, món phở bò này thơm ngon quá, ăn một bát là nhớ mãi!",
    "Bánh mì giòn rụm kẹp thịt nướng thơm phức là món tôi thích nhất.",
    "Chị ấy nấu canh chua cá lóc ngon đến mức ai ăn cũng phải khen.",
    "Ly trà đá mát lạnh giữa trưa hè oi ả thật là dễ chịu.",
    "Hương vị cà phê sữa đá Sài Gòn đậm đà khó quên.",

    # --- Câu hỏi ---
    "Bạn có khỏe không? Lâu rồi chúng ta chưa gặp lại nhau.",
    "Tại sao bầu trời lại có màu xanh vào ban ngày nhỉ?",
    "Cuối tuần này bạn có muốn đi xem phim cùng tôi không?",
    "Bạn đã ăn sáng chưa, hay là chúng ta đi ăn cùng nhau?",
    "Liệu ngày mai trời có mưa để tôi mang theo áo khoác không?",
    "Cậu nghĩ sao về kế hoạch du lịch Đà Lạt vào tháng sau?",

    # --- Cảm thán, cảm xúc ---
    "Tuyệt vời quá, cuối cùng chúng ta cũng hoàn thành dự án rồi!",
    "Trời ơi, cảnh hoàng hôn ở đây đẹp đến nghẹt thở luôn!",
    "Thật đáng tiếc, trận đấu kết thúc với tỉ số hòa đáng tiếc.",
    "Tôi vui lắm khi nghe tin bạn đã thi đỗ vào trường mơ ước.",
    "Ôi chao, em bé cười tươi quá làm ai cũng thấy ấm lòng.",

    # --- Số, ngày tháng, đo lường ---
    "Quyển sách dày bốn trăm trang ấy kể về hành trình vượt đại dương.",
    "Buổi họp được dời sang chín giờ ba mươi phút ngày mai.",
    "Lượng mưa năm nay cao hơn trung bình nhiều năm khoảng mười lăm phần trăm.",
    "Chuyến bay khởi hành lúc sáu giờ bốn mươi lăm phút sáng thứ Hai.",
    "Tổng chi phí dự án ước tính khoảng hai tỷ ba trăm triệu đồng.",
    "Quãng đường từ Hà Nội vào Huế dài khoảng sáu trăm năm mươi cây số.",
    "Nhiệt độ ngoài trời hôm nay là ba mươi hai độ C, khá nóng.",
    "Lớp tôi có bốn mươi hai học sinh, trong đó hai mươi ba bạn nữ.",

    # --- Công việc, học tập, công nghệ ---
    "Khoa học và công nghệ đang thay đổi cuộc sống của chúng ta từng ngày.",
    "Chúng tôi đã hoàn thành dự án đúng hạn nhờ sự nỗ lực của cả nhóm.",
    "Phần mềm này hỗ trợ nhận diện giọng nói bằng tiếng Việt khá tốt.",
    "Trí tuệ nhân tạo giúp tự động hóa nhiều công việc lặp đi lặp lại.",
    "Em cần ôn lại bài kỹ càng trước kỳ thi học kỳ sắp tới.",
    "Anh ấy thuyết trình rất tự tin và thuyết phục trước hội đồng.",
    "Dữ liệu được mã hóa cẩn thận để bảo vệ quyền riêng tư người dùng.",
    "Cuộc cách mạng số đòi hỏi mỗi người không ngừng học hỏi cái mới.",

    # --- Cảnh vật, địa danh ---
    "Đường phố Sài Gòn về đêm lung linh ánh đèn và nhộn nhịp người qua lại.",
    "Vịnh Hạ Long với hàng nghìn hòn đảo đá vôi là kỳ quan thiên nhiên.",
    "Phố cổ Hội An rực rỡ sắc màu đèn lồng trong đêm rằm.",
    "Ruộng bậc thang Sa Pa uốn lượn như những nấc thang lên trời.",
    "Chợ nổi miền Tây tấp nập ghe thuyền chở đầy hoa trái.",

    # --- Câu chứa từ khó phát âm / ghép phụ âm ---
    "Nghìn nghịt người chen chúc khuỳnh khoàng giữa ngã tư đông đúc.",
    "Khúc khuỷu gập ghềnh, con đường mòn ngoằn ngoèo lên đỉnh dốc.",
    "Quệt nhẹ giọt sương, nhánh nguyệt quế khẽ rung rinh trong gió.",
    "Thuyền trưởng nghiêm nghị khuyến khích thủy thủ giữ vững tay lái.",
    "Chuyến nghỉ dưỡng tuyệt vời khiến chúng tôi khuây khỏa hẳn.",

    # --- Tục ngữ, thành ngữ, văn nói ---
    "Có công mài sắt, có ngày nên kim, cứ kiên trì rồi sẽ thành công.",
    "Đi một ngày đàng, học một sàng khôn, trải nghiệm là thầy giỏi nhất.",
    "Uống nước nhớ nguồn, ăn quả nhớ kẻ trồng cây bạn nhé.",
    "Một cây làm chẳng nên non, ba cây chụm lại nên hòn núi cao.",
    "Lá lành đùm lá rách là truyền thống quý báu của dân tộc ta.",

    # --- Kể chuyện, miêu tả dài hơn ---
    "Những đứa trẻ nô đùa vui vẻ giữa sân trường rợp bóng cây bàng.",
    "Tiếng đàn ghi ta vang lên dìu dặt trong đêm trăng thanh vắng.",
    "Vườn hoa rực rỡ đủ sắc màu, nào hồng, nào cúc, nào lan, nào huệ.",
    "Bà cụ ngồi têm trầu bên hiên nhà, ánh mắt hiền từ nhìn xa xăm.",
    "Đoàn tàu rời ga trong tiếng còi vang vọng, mang theo bao nỗi nhớ.",
    "Cậu bé say sưa ngắm đàn cá vàng bơi lội tung tăng trong bể.",
    "Người thợ rèn cần mẫn quai búa, lửa lò bừng sáng cả góc xưởng.",
    "Cơn gió thu se lạnh luồn qua khe cửa, mang theo mùi hoa sữa.",

    # --- Động viên, triết lý nhẹ ---
    "Tôi tin rằng chỉ cần cố gắng thì khó khăn nào rồi cũng sẽ qua.",
    "Hãy giữ gìn sức khỏe và luôn mỉm cười với cuộc sống bạn nhé.",
    "Thất bại chỉ là bài học để ta trưởng thành và mạnh mẽ hơn.",
    "Mỗi ngày trôi qua đều là một món quà quý giá của cuộc sống.",
    "Đừng ngại bắt đầu lại, miễn là bạn không bao giờ bỏ cuộc.",
    "Lòng tốt nhỏ bé cũng có thể sưởi ấm cả một trái tim lạnh giá.",

    # --- Đối thoại, tình huống ---
    "Cho tôi hỏi đường ra ga tàu đi lối nào ạ, tôi bị lạc rồi.",
    "Bạn vui lòng nói chậm lại một chút để tôi ghi chép kịp nhé.",
    "Xin lỗi đã làm phiền, bạn có thể giúp tôi một việc nhỏ không?",
    "Để tôi gọi điện xác nhận lại lịch hẹn với khách hàng đã.",
    "Anh chị cứ ngồi nghỉ ngơi, đồ uống sẽ được mang ra ngay thôi.",
    "Chúc mừng sinh nhật, mong mọi điều tốt đẹp nhất đến với bạn!",

    # --- Bổ sung đa dạng âm cuối ---
    "Ánh nắng ban mai chiếu rọi khắp con hẻm nhỏ rộn ràng tiếng rao.",
    "Bát canh nóng hổi tỏa khói nghi ngút giữa ngày đông giá rét.",
    "Tiếng trống trường giòn giã báo hiệu giờ ra chơi đã đến.",
    "Đám mây hồng tím cuối chân trời báo hiệu một buổi chiều tà.",
    "Hạt mưa lất phất rơi trên mái ngói rêu phong cổ kính.",

    # === Bổ sung để đạt 200 câu ===

    # --- Gia đình, tình cảm ---
    "Cha tôi là một người đàn ông trầm tính nhưng vô cùng ấm áp.",
    "Mỗi dịp Tết đến, cả gia đình lại sum họp gói bánh chưng xanh.",
    "Em gái tôi học lớp tám và rất giỏi môn vẽ tranh phong cảnh.",
    "Ông nội thường ngồi tỉa cây cảnh ngoài sân vào mỗi buổi chiều.",
    "Tình bạn chân thành là điều quý giá mà tiền bạc không mua được.",
    "Vợ chồng son sẻ dắt nhau đi dạo công viên dưới hàng cây xanh mát.",
    "Đứa cháu nhỏ bi bô tập nói khiến cả nhà ai cũng bật cười.",
    "Người mẹ tảo tần thức khuya dậy sớm lo cho đàn con ăn học.",
    "Hai anh em cãi nhau chí chóe nhưng lại thương nhau vô cùng.",
    "Bữa cơm đoàn viên cuối năm là khoảnh khắc ấm áp nhất với tôi.",

    # --- Du lịch, trải nghiệm ---
    "Chúng tôi cắm trại bên bờ suối, nướng khoai và ngắm sao trời.",
    "Hành trình phượt xuyên Việt để lại trong tôi vô vàn kỷ niệm đẹp.",
    "Bãi biển hoang sơ với cát trắng mịn và nước biển xanh trong vắt.",
    "Tôi leo lên đỉnh Fansipan và ngắm biển mây bồng bềnh tuyệt đẹp.",
    "Phiên chợ vùng cao rực rỡ sắc màu thổ cẩm của người dân tộc.",
    "Đêm Đà Lạt se lạnh, chúng tôi ngồi quây quần bên bếp lửa hồng.",
    "Con đò nhỏ lặng lẽ đưa khách sang sông trong buổi sớm mờ sương.",
    "Khu rừng nguyên sinh ẩn chứa biết bao loài chim thú quý hiếm.",
    "Thác nước tung bọt trắng xóa đổ ầm ầm xuống lòng hồ sâu thẳm.",
    "Chuyến đi biển lần này khiến tôi thấy yêu quê hương mình hơn.",

    # --- Sức khỏe, thể thao ---
    "Mỗi sáng tôi đều dậy sớm chạy bộ và hít thở không khí trong lành.",
    "Tập yoga đều đặn giúp tinh thần thư thái và cơ thể dẻo dai hơn.",
    "Bác sĩ khuyên tôi nên ăn nhiều rau xanh và uống đủ hai lít nước.",
    "Đội bóng quê tôi đã giành chiến thắng vang dội trong trận chung kết.",
    "Ngủ đủ giấc và ăn uống điều độ là bí quyết để khỏe mạnh dài lâu.",
    "Vận động viên ấy đã phá kỷ lục quốc gia ở nội dung chạy cự ly dài.",
    "Đi bộ mười nghìn bước mỗi ngày rất tốt cho hệ tim mạch của bạn.",
    "Hãy nhớ khởi động kỹ trước khi tập luyện để tránh chấn thương.",

    # --- Nghề nghiệp, xã hội ---
    "Người nông dân cần mẫn ra đồng từ tờ mờ sáng để chăm sóc lúa.",
    "Cô giáo tận tụy giảng bài, ánh mắt ngời sáng niềm say mê.",
    "Anh kỹ sư miệt mài bên bản vẽ để hoàn thiện cây cầu mới.",
    "Bác sĩ trực đêm vẫn ân cần thăm khám cho từng bệnh nhân.",
    "Người lính canh giữ biên cương, vững vàng giữa nắng gió biên thùy.",
    "Chị công nhân vệ sinh lặng lẽ làm sạch phố phường mỗi đêm khuya.",
    "Anh shipper rong ruổi khắp ngả đường để giao hàng kịp giờ hẹn.",
    "Người thợ mộc khéo léo chạm khắc hoa văn tinh xảo lên thớ gỗ.",
    "Nghề giáo là nghề cao quý, ươm mầm tri thức cho bao thế hệ.",
    "Bác tài xế đường dài tỉnh táo ôm vô lăng suốt chặng đường xa.",

    # --- Văn hóa, nghệ thuật ---
    "Tiếng sáo trúc du dương vọng lại từ phía bên kia triền đê.",
    "Bức tranh sơn mài lấp lánh ánh vàng dưới ánh đèn bảo tàng.",
    "Vở chèo cổ được các nghệ sĩ trình diễn say sưa giữa sân đình.",
    "Câu hát ru ngọt ngào đưa em bé chìm vào giấc ngủ êm đềm.",
    "Lễ hội đua thuyền rồng thu hút hàng nghìn người đến cổ vũ.",
    "Nghệ nhân nặn tò he thoăn thoắt tạo ra những hình thù ngộ nghĩnh.",
    "Điệu múa xòe Thái uyển chuyển bên ánh lửa trại bập bùng.",
    "Tranh Đông Hồ gà lợn nét tươi trong, màu dân tộc sáng bừng giấy điệp.",

    # --- Số liệu, thông báo, tin tức ---
    "Dân số thành phố đã vượt mốc chín triệu người vào năm ngoái.",
    "Giá xăng dầu tuần này tăng thêm khoảng một nghìn hai trăm đồng mỗi lít.",
    "Kỳ nghỉ lễ kéo dài bốn ngày, từ thứ Bảy đến hết thứ Ba tuần sau.",
    "Cửa hàng mở cửa từ tám giờ sáng đến mười giờ tối tất cả các ngày.",
    "Tỉ lệ học sinh tốt nghiệp năm nay đạt chín mươi tám phẩy năm phần trăm.",
    "Hội chợ triển lãm sẽ diễn ra tại trung tâm vào ngày mười hai tháng Tư.",
    "Đơn hàng của bạn dự kiến được giao trong vòng ba đến năm ngày tới.",
    "Nhiệt độ ban đêm có thể giảm xuống chỉ còn mười tám độ C.",
    "Tuyến xe buýt số bốn mươi hai chạy qua mười bảy điểm dừng.",
    "Chương trình giảm giá áp dụng cho hóa đơn từ năm trăm nghìn đồng.",

    # --- Câu hỏi, đối thoại bổ sung ---
    "Bạn có thể chỉ giúp tôi cách đi đến bưu điện gần nhất không?",
    "Chúng ta nên chọn nhà hàng nào cho buổi tiệc tối nay đây?",
    "Cậu đã hoàn thành bài tập nhóm mà thầy giao hôm qua chưa?",
    "Liệu tôi có thể đổi sang chuyến tàu sớm hơn được không ạ?",
    "Bạn thích mùa nào nhất trong bốn mùa xuân, hạ, thu, đông?",
    "Tại sao hôm nay cậu lại đến lớp muộn hơn thường lệ vậy?",
    "Mình nên mang theo những gì cho chuyến đi cắm trại cuối tuần?",
    "Anh ơi, quán cà phê này còn chỗ ngồi ngoài ban công không?",

    # --- Cảm thán, biểu cảm bổ sung ---
    "Chao ôi, cánh đồng hoa hướng dương vàng rực đẹp như tranh vẽ!",
    "Thật bất ngờ, món quà nhỏ của bạn khiến tôi xúc động vô cùng!",
    "Hú hồn, suýt chút nữa là tôi đã làm rơi chiếc bình quý rồi!",
    "Quá đỉnh, đội tuyển nhà mình vừa ghi bàn thắng ở phút cuối cùng!",
    "Tiếc thật đấy, giá mà chúng ta đến sớm hơn mười phút thôi nhỉ.",
    "Ôi trời, sao hôm nay đường lại tắc nghẽn kinh khủng đến thế này!",

    # --- Từ khó, ghép phụ âm bổ sung ---
    "Khúc nhạc nguyệt cầm nỉ non trầm bổng giữa khuya khoắt tĩnh mịch.",
    "Ngoằn ngoèo theo triền núi, dòng suối uốn lượn quanh co khúc khuỷu.",
    "Chàng trai khẳng khái, quả quyết khước từ mọi lời dụ dỗ ngon ngọt.",
    "Quệt mồ hôi, người thợ tiếp tục khuân vác những thùng hàng nặng trịch.",
    "Tuyết phủ trắng xóa khắp khu rừng, cảnh vật im lìm khô khốc.",
    "Nguyễn Khuyến là nhà thơ nức tiếng với chùm thơ thu trữ tình.",
    "Khuýp khuỳu, lũ trẻ rón rén luồn qua khe cổng hẹp để trốn tìm.",
    "Quỳnh hương khe khẽ nở trong đêm, tỏa hương thơm ngào ngạt.",

    # --- Tục ngữ, ca dao bổ sung ---
    "Gần mực thì đen, gần đèn thì sáng, chọn bạn mà chơi bạn nhé.",
    "Thương người như thể thương thân, sống sao cho trọn nghĩa tình.",
    "Tốt gỗ hơn tốt nước sơn, xấu người đẹp nết còn hơn đẹp người.",
    "Nước chảy đá mòn, kiên trì bền bỉ ắt có ngày thành công.",
    "Ăn vóc học hay, chịu khó rèn luyện thì tài năng sẽ nảy nở.",
    "Bầu ơi thương lấy bí cùng, tuy rằng khác giống nhưng chung một giàn.",

    # --- Kể chuyện, miêu tả dài bổ sung ---
    "Ông lão đánh cá thả lưới giữa biển khơi mênh mông sóng nước.",
    "Cô bé quàng khăn đỏ tung tăng băng qua khu rừng đầy nắng.",
    "Chàng tiều phu cần mẫn đốn củi rồi gánh xuống chợ phiên bán.",
    "Đàn cò trắng chao nghiêng trên cánh đồng lúa vàng buổi hoàng hôn.",
    "Cụ bà ngồi đan len bên cửa sổ, len màu đỏ cuộn tròn dưới chân.",
    "Bầy trẻ thả diều trên triền đê lộng gió chiều quê thanh bình.",
    "Người họa sĩ già lặng lẽ phác họa khung cảnh phố phường tấp nập.",
    "Cơn bão đi qua để lại những hàng cây ngả nghiêng xơ xác lá.",
    "Chiếc đồng hồ quả lắc cũ kỹ vẫn đều đặn điểm từng tiếng chuông.",
    "Khói lam chiều bảng lảng trên những nóc nhà tranh ven sông.",

    # --- Động viên, suy ngẫm bổ sung ---
    "Thành công không đến từ may mắn mà từ sự nỗ lực không ngừng nghỉ.",
    "Hãy sống hết mình hôm nay, vì ngày mai là điều không ai đoán trước.",
    "Một nụ cười bằng mười thang thuốc bổ, hãy luôn lạc quan bạn nhé.",
    "Khó khăn rồi sẽ qua đi, điều ở lại là bản lĩnh ta tôi luyện được.",
    "Đọc một cuốn sách hay cũng như trò chuyện với một người bạn hiền.",
    "Biết đủ là giàu, sống an nhiên thì lòng mới thật sự bình yên.",
    "Gieo suy nghĩ gặt hành động, gieo thói quen gặt cả số phận đời mình.",
    "Mỗi sai lầm đều dạy ta một điều, miễn là ta chịu lắng nghe nó.",

    # --- Thời tiết, mùa bổ sung ---
    "Mùa xuân về, muôn hoa đua nở khoe sắc thắm khắp các nẻo đường.",
    "Nắng hè chói chang trải vàng trên những tán phượng vĩ đỏ rực.",
    "Heo may chớm lạnh, mùi cốm non thoang thoảng gọi thu Hà Nội.",
    "Đông sang, gió bấc thổi từng cơn buốt giá qua khung cửa sổ.",
    "Sấm chớp đì đùng báo hiệu một cơn giông lớn sắp ập đến nơi.",
    "Cầu vồng bảy sắc hiện ra rực rỡ sau cơn mưa rào mùa hạ.",

    # --- Sinh hoạt, đời thường bổ sung ---
    "Tôi tranh thủ tưới mấy chậu hoa trước khi ánh nắng lên cao.",
    "Cô bán hàng niềm nở gói ghém cẩn thận từng món đồ cho khách.",
    "Tiếng rao đêm văng vẳng khắp con phố nhỏ tĩnh lặng về khuya.",
    "Tôi xếp gọn sách vở lên giá rồi lau dọn lại căn phòng cho ngăn nắp.",
    "Mùi bánh nướng thơm lừng lan tỏa khắp gian bếp ngày giáp Tết.",
    "Chiếc quạt trần quay đều kẽo kẹt trong buổi trưa hè oi ả.",
    "Bà hàng nước pha trà mời khách, khói trà bay nhè nhẹ trong gió.",
    "Tôi ngồi nhâm nhi tách trà nóng, lắng nghe tiếng mưa rơi tí tách.",
]
