import { legacy_createStore as createStore } from 'redux';

const initialState = {
  data: null,
};

function reducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_DATA':
      return {
        ...state,
        data: action.payload,
      };
    default:
      return state;
  }
}

export const store = createStore(reducer);
