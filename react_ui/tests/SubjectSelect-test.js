/* global define, it, describe */
import React from 'react';
import { mount, shallow, render } from 'enzyme';
import { expect } from 'chai';

import { SubjectSelect } from '../components/SubjectSelect';
import { Provider } from 'react-redux';

import store from './test-store';


describe('<SubjectSelect/>', () => {
  const SubSelectProps = {
    store,
    protocol: {
      items: [],
      activeProtocolId: 1,
      orgs: [],
    },
    subject: {
      items: [],
      addSubjectMode: false,
      isFetching: false,
    },
  };
  it('should contain an h3 header', () => {
    const wrapper = shallow(<SubjectSelect params={{ id: 1 }} {...SubSelectProps} />);
    expect(wrapper.contains('<h3>'));
  });
});
