import React from "react";
import { FormattedMessage } from "react-intl";
import CloudLabel from "components/CloudLabel";
import { sortObjects } from "utils/arrays";
import { REGION_BE_FILTER, REGION_FILTER } from "utils/constants";
import Filter from "../Filter";

class RegionFilter extends Filter {
  static filterName = REGION_FILTER;

  static apiName = REGION_BE_FILTER;

  static displayedName = (<FormattedMessage id="region" />);

  static _getValue(filterItem) {
    return filterItem.name;
  }

  static _getDisplayedValueRenderer(filterItem, props) {
    return <CloudLabel name={filterItem.name} type={filterItem.cloud_type} disableLink {...props} />;
  }

  _getAppliedFilterItem(appliedFilter, filterItem) {
    return {
      value: appliedFilter,
      displayedValue: this.constructor.getDisplayedValueRenderer(filterItem, () => ({
        iconProps: {
          dataTestId: `${this.constructor.filterName}_filter_logo`
        }
      }))
    };
  }

  static _sortFilterValues(items) {
    return sortObjects({
      array: items,
      field: "name",
      type: "asc"
    });
  }
}

export default RegionFilter;
