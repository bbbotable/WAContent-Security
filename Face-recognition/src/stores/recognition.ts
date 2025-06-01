import axios from "axios";

export async function UserSignUp(blob: Blob, option: string, time: string): Promise<string> {
    const formData = new FormData()
    formData.append('image', blob, 'photo.png')

    // 尝试人脸识别
    let name = ''
    let student_id = ''
    let recognition_success = false
    let liveness_success = false
    let result = ''

    try {
        const faceRes = await axios.post('http://localhost:5000/face/recognition', formData)
        console.log('人脸识别结果:', faceRes.data)
        recognition_success = faceRes.data?.state || false

        if (!recognition_success) throw new Error(faceRes.data?.message || '识别失败')

        name = faceRes.data.name || ''
        student_id = faceRes.data.student_id || ''
    } catch (e) {
        result = '识别失败'
    }

    // 活体检测（只有识别成功后才尝试）
    if (recognition_success) {
        try {
            const liveRes = await axios.post(`http://localhost:5000/liveness/${option}`, formData)
            console.log('活体检测结果:', liveRes.data)
            liveness_success = liveRes.data?.liveness_passed || false
            if (!liveness_success) {
                result = '未通过活体检测'
            }
        } catch (e) {
            result = '活体检测错误'
        }
    }

    // 最终判断
    if (recognition_success && liveness_success) {
        result = name+' 签到成功'
    }

    // 提交签到记录
    const recordForm = new FormData()
    recordForm.append('image', blob, 'photo.png')
    recordForm.append('time', time)
    recordForm.append('result', result)
    recordForm.append('recognition_success', recognition_success.toString())
    recordForm.append('liveness_success', liveness_success.toString())
    recordForm.append('name', name)
    recordForm.append('student_id', student_id)
    console.log('📦 签到记录信息：')
    console.log('time:', time)
    console.log('result:', result)
    console.log('recognition_success:', recognition_success)
    console.log('liveness_success:', liveness_success)
    console.log('name:', name)
    console.log('student_id:', student_id)


    await axios.post('http://localhost:5000/face/record', recordForm)

    return result
}
