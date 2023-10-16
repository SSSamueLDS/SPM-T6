import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
    state: {
        all_skills: [],
        all_dept: [],
        all_roles: []
    },
    mutations: {
        setAllSkills(state, data) {
            state.all_skills = data;
        },
        setAllDept(state, data) {
            state.all_dept = data;
        },
        setAllRoles(state, data) {
            state.all_roles = data;
        },
    },
    actions: {
        async fetchAllSkills({ commit }) {
            const response = await axios.get('http://127.0.0.1:5003/skills');
            commit('setAllSkills', response.data.data);
        },
        async fetchAllDept({ commit }) {
            const response = await axios.get('http://127.0.0.1:5004/staffs/dept');
            commit('setAllDept', response.data.data);
        },
        async fetchAllRoles({ commit }) {
            const response = await axios.get('http://127.0.0.1:5005/roles');
            commit('setAllRoles', response.data.data);
        }
    }
});
