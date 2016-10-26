/* global define, it, describe */
import React from 'react';
import { mount, shallow, render } from 'enzyme';
import { expect } from 'chai';

import SubjectSelect from '../components/SubjectSelect';
import { Provider } from 'react-redux';
import store from '../store';


describe('<SubjectSelect/>', () => {
  const SubSelectProps = {
    store,
  };
  it('should contain an h3 header', () => {
    // console.log(render(<SubjectSelect {...SubSelectProps} />))
    const wrapper = shallow(<SubjectSelect {...SubSelectProps} />);
    expect(wrapper.contains('<h3>'));
  });
});
