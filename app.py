from flask import Flask, jsonify

app = Flask(__name__)

# متغير لتتبع حالة الـ LED الحالية.
# (سيفقد هذا المتغير قيمته عند إعادة تشغيل الخادم، لكنه يكفي للتحكم الأساسي)
current_led_state = "off"

@app.route('/', methods=['GET'])
def index():
    """ 
    نقطة نهاية (Endpoint) أساسية للتحقق من أن الخادم يعمل.
    """
    return jsonify({
        "status": "Running",
        "service": "SIM7600 LED Control API",
        "current_led_state": current_led_state
    })

@app.route('/led/<action>', methods=['GET'])
def control_led(action):
    """
    نقطة النهاية الرئيسية التي يستدعيها الأردوينو.
    المسار المتوقع: /led/on أو /led/off
    """
    global current_led_state
    
    action = action.lower() # تحويل الإجراء إلى حروف صغيرة
    
    if action == "on":
        current_led_state = "on"
        print(f"**LOG: Received 'ON' command.** New state: {current_led_state}")
        return jsonify({"command_received": action, "new_state": current_led_state, "result": "Success"}), 200
    
    elif action == "off":
        current_led_state = "off"
        print(f"**LOG: Received 'OFF' command.** New state: {current_led_state}")
        return jsonify({"command_received": action, "new_state": current_led_state, "result": "Success"}), 200
        
    else:
        # استجابة في حالة إرسال أمر غير صحيح
        return jsonify({"result": "Error", "message": "Invalid action. Use 'on' or 'off'."}), 400

if __name__ == '__main__':
    # Render سيستخدم متغير البيئة PORT لتشغيل التطبيق
    # يمكنك استخدام 5000 للاختبار المحلي
    app.run(host='0.0.0.0', port=5000)