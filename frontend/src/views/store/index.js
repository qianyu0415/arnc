import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    // 其他状态
    processedFileName: '', // 用于存储文件名的状态
  },
  mutations: {
    // 其他mutations
    SET_PROCESSED_FILE_NAME(state, fileName) {
      state.processedFileName = fileName;
    }
  },
  actions: {
    // 其他actions
    setProcessedFileName({ commit }, fileName) {
      commit('SET_PROCESSED_FILE_NAME', fileName);
    }
  }
});

  
