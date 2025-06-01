import axios from "axios";
import { defineStore } from 'pinia'


export const useSignStore = defineStore('sign',{
    state:()=>({
        signs:[],
    }),
    actions:{
        async loadSigns() {
        const res = await axios.get('http://localhost:5000/face/signinrecord')
        this.signs = res.data
        },
        async deleteSign(id:number) {
        await axios.delete(`http://localhost:5000/face/deletesign/${id}`)
        await this.loadSigns()
        },
    }
})

export async function getStats() {
    const res = await fetch('http://localhost:5000/face/stats')
    const data = await res.json()
    return data
}