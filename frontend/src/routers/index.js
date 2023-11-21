import { createRouter, createWebHistory } from 'vue-router'


const routers = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path:"/",
            name:"Index",
            component: ()=>import('../views/index.vue')
        },
        {
            path:"/register",
            name:"Register",
            component: ()=>import('../views/Register.vue')
        },
        {
            path:"/login",
            name:"Login",
            component: () => import('../views/Login.vue')
        },
        {
            path: "/home",
            name: "Home",
            component: () => import('../views/Home.vue')
        },
    ]

})

export default routers


