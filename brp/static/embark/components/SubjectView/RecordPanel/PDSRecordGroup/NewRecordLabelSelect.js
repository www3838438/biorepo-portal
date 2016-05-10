// jscs:disable requireCamelCaseOrUpperCaseIdentifiers
import React from 'react';
import SelectField from 'material-ui/lib/select-field';
import MenuItem from 'material-ui/lib/menus/menu-item';
import RaisedButton from 'material-ui/lib/raised-button';
import LoadingGif from '../../../LoadingGif';
import * as RecordActions from '../../../../actions/record';

import { connect } from 'react-redux';

class NewRecordLabelSelect extends React.Component {

  constructor(props) {
    super(props);
    this.handleRecordLabelSelect = this.handleRecordLabelSelect.bind(this);
    this.handleNewRecordClick = this.handleNewRecordClick.bind(this);
  }

  handleRecordLabelSelect(e, index, value) {
    const { dispatch } = this.props;
    dispatch(RecordActions.setSelectedLabel(value));
  }

  handleNewRecordClick() {
    const { dispatch } = this.props;
    if (this.props.selectedLabel === null) {
      dispatch(RecordActions.setRecordError('Please select a record label.'));
      return;
    }
    dispatch(RecordActions.createRecordRequest());
    const url = `/dataentry/protocoldatasource/${this.props.pds.id}/subject/` +
      `${this.props.subject.id}/create/?label_id=${this.props.selectedLabel}`;
    window.location.href = url;
  }

  render() {
    const labels = this.props.pds.driver_configuration.labels;

    return (
      this.props.isCreating ?
        <div>
          <h4 style={{ textAlign: 'center' }}>
            Please wait. This action may take several seconds...
          </h4>
          <LoadingGif />
        </div> :
        <div>
          <div>
            <span>Select label for {this.props.pds.display_label} Record:</span>
            <SelectField
              onChange={this.handleRecordLabelSelect}
              style={{ width: '100%' }}
              value={this.props.selectedLabel}
            >
              {labels.map((label, i) => (
                <MenuItem key={i} value={label[0]} primaryText={label[1]} />
              ))}
            </SelectField>
          </div>
          <div>
            <RaisedButton
              onClick={this.handleNewRecordClick}
              label={'Create New'}
              labelColor={'#7AC29A'}
              type="submit"
              style={{ width: '100%' }}
            />
          </div>
          {this.props.newRecordError != null ?
            <div className="alert alert-danger">{this.props.newRecordError}</div>
          : null}
        </div>
    );
  }
}

NewRecordLabelSelect.propTypes = {
  dispatch: React.PropTypes.func,
  subject: React.PropTypes.object,
  selectedLabel: React.PropTypes.number,
  pds: React.PropTypes.object,
  isCreating: React.PropTypes.bool,
  newRecordError: React.PropTypes.string,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    selectedLabel: state.record.selectedLabel,
    isCreating: state.record.isCreating,
    newRecordError: state.record.newRecordError,
  };
}

export default connect(mapStateToProps)(NewRecordLabelSelect);
