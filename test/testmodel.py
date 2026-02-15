from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

# تحميل النموذج
model = load_model('models\\Bone-Fracture-Detection---MURA-master\\save_models\\MURA_modle@epochs50.h5', compile=False)

# تعريف المحسن يدويًا
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# تأكد من أن النموذج تم تحميله بشكل صحيح عن طريق اختبار التنبؤ
import numpy as np
from tensorflow.keras.preprocessing import image

# تحميل صورة للاختبار (استبدل المسار بالصورة التي تريد اختبارها)
# تعريف الأبعاد المطلوبة للصورة
IMG_HEIGHT = 224  # أو أي قيمة أخرى حسب ما يحتاجه النموذج
IMG_WIDTH = 224   # أو أي قيمة أخرى حسب ما يحتاجه النموذج

# تحميل صورة للاختبار
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2

# مسار الصورة
img_path = 'test.png'

# تحميل الصورة وتغيير حجمها إلى 320x320
img = image.load_img(img_path, target_size=(320, 320), color_mode='grayscale')

# تحويل الصورة إلى مصفوفة NumPy
img_array = image.img_to_array(img)

# إضافة بعد جديد لتتناسب مع الشكل الذي يتوقعه النموذج (1, 320, 320, 1)
img_array = np.expand_dims(img_array, axis=0)

# تطبيع القيم لتتراوح بين 0 و 1
img_array /= 255.0

# التنبؤ باستخدام النموذج
prediction = model.predict(img_array)

# طباعة النتيجة
print(prediction)
