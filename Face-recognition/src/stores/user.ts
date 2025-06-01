import axios from "axios";
import { defineStore } from 'pinia'

export async function LoginUser(username:string,password:string):Promise<string> {
    const response = await axios.post('http://localhost:5000/user/login',{username,password});
    if(response.data?.token){
        return response.data.token;
    }else{
        throw new Error('登录失败');
    }
}
export const useUserStore = defineStore('user',{
    state:()=>({
        users:[],
    }),
    actions:{
        async loadUsers() {
        const res = await axios.get('http://localhost:5000/face/list')
        this.users = res.data
        },
        async deleteUser(id:number) {
        await axios.delete(`http://localhost:5000/face/delete/${id}`)
        await this.loadUsers()
        },
        async uploadUser({ name, student_id, photo }: { name: string; student_id: string; photo: File }) {
        const formData = new FormData()
        formData.append('name', name)
        formData.append('student_id', student_id)
        formData.append('photo', photo)
        await axios.post('http://localhost:5000/face/upload', formData)
        await this.loadUsers()
        }
    }
})