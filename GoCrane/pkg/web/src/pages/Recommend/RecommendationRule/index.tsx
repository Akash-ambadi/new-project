import {
  RecommendationRuleSimpleInfo,
  useFetchRecommendationRuleListQuery,
} from '../../../services/recommendationRuleApi';
import CommonStyle from '../../../styles/common.module.less';
import SearchForm from './components/SearchForm';
import './index.module.less';
import JsYaml from 'js-yaml';
import classnames from 'classnames';
import { useCraneUrl } from 'hooks';
import React, { memo, useState } from 'react';
import { Button, Col, Dialog, Divider, MessagePlugin, Row, Space, Table, Tag } from 'tdesign-react';
import { useTranslation } from 'react-i18next';

const Editor = React.lazy(() => import('components/common/Editor'));

export const SelectTable = () => {
  const { t } = useTranslation();
  const [yamlDialogVisible, setYamlDialogVisible] = useState<boolean>(false);
  const [currentSelection, setCurrentSelection] = useState<RecommendationRuleSimpleInfo | null>(null);
  const [selectedRowKeys, setSelectedRowKeys] = useState<(string | number)[]>([0, 1]);
  const [visible, setVisible] = useState(false);
  const [filterParams, setFilterParams] = useState({
    recommenderType: undefined,
    name: undefined,
  });
  const craneUrl: any = useCraneUrl();
  const { data, isFetching, isError, isSuccess, error } = useFetchRecommendationRuleListQuery({ craneUrl });
  let recommendationRuleList: any[];
  if (isSuccess) {
    recommendationRuleList = data?.data?.items || [];
  } else {
    recommendationRuleList = [];
    if (isError) MessagePlugin.error(`${error.status} ${error.error}`);
  }
  const filterResult = recommendationRuleList
    .filter((recommendationRule) => {
      console.log(recommendationRule);
      if (filterParams?.name) {
        return new RegExp(`${filterParams.name}.*`).test(recommendationRule.name);
      }
      return true;
    })
    .filter((recommendationRule) => {
      if (filterParams?.recommenderType) return filterParams?.recommenderType === recommendationRule.recommenderType;
      return true;
    });

  function onSelectChange(value: (string | number)[]) {
    setSelectedRowKeys(value);
  }

  function rehandleClickOp(record: any) {
    console.log(record);
  }

  function handleClickDelete(record: any) {
    console.log(record);
    setVisible(true);
  }

  function handleClose() {
    setVisible(false);
  }

  const toYaml = (resource: any) => {
    let yaml = null;
    try {
      yaml = JsYaml.dump(resource);
    } catch (error) {
      //
    }
    return yaml;
  };

  return (
    <>
      {/* <Row>
        <Button disabled>{t('??????????????????')}</Button>
      </Row>
      <Divider></Divider> */}
      <Row justify='start' style={{ marginBottom: '20px' }}>
        <Col>
          <SearchForm filterParams={filterParams} setFilterParams={setFilterParams} />
        </Col>
      </Row>
      <Table
        loading={isFetching || isError}
        data={filterResult}
        columns={[
          {
            title: t('??????'),
            colKey: 'metadata.name',
          },
          {
            title: t('????????????'),
            ellipsis: true,
            colKey: 'spec.recommenders',
            cell({ row }) {
              return (
                <Space direction='vertical'>
                  {row.spec.recommenders.map((recommender) => {
                    if (recommender.name === 'Replicas')
                      return (
                        <Tag theme='warning' variant='light'>
                          {recommender.name}
                        </Tag>
                      );
                    if (recommender.name === 'Resource')
                      return (
                        <Tag theme='primary' variant='light'>
                          {recommender.name}
                        </Tag>
                      );
                  })}
                </Space>
              );
            },
          },
          {
            title: t('????????????'),
            width: 300,
            ellipsis: true,
            colKey: 'spec.resourceSelectors',
            cell({ row }) {
              const { resourceSelectors } = row.spec;
              return (
                <Space direction='vertical'>
                  {resourceSelectors.map((o: { kind: string; name: string }, i: number) => (
                    <Tag key={i} theme='success' variant='light'>
                      {o.kind}
                      {o.name ? ' / ' : ''}
                      {o.name ?? ''}
                    </Tag>
                  ))}
                </Space>
              );
            },
          },
          {
            title: t('Namespace ?????????'),
            ellipsis: true,
            colKey: 'spec.namespaceSelector',
            cell({ row }) {
              const ns = row.spec.namespaceSelector;
              if (ns?.any) return 'Any';
              return ns.matchNames;
            },
          },
          {
            title: t('????????????'),
            ellipsis: true,
            colKey: 'spec.runInterval',
          },
          {
            title: t('????????????'),
            ellipsis: true,
            colKey: 'metadata.creationTimestamp',
            cell({ row }) {
              const tmp = new Date(row.metadata.creationTimestamp);
              return `${tmp.toLocaleDateString()} ${tmp.toLocaleTimeString()}`;
            },
          },
          {
            align: 'left',
            fixed: 'right',
            width: 200,
            colKey: 'op',
            title: t('??????'),
            cell(record) {
              return (
                <>
                  {/* <Button
                    theme='primary'
                    variant='text'
                    onClick={() => {
                      rehandleClickOp(record);
                    }}
                    disabled={true}
                  >
                    {t('??????')}
                  </Button>
                  <Button
                    theme='primary'
                    variant='text'
                    disabled={true}
                    onClick={() => {
                      handleClickDelete(record);
                    }}
                  >
                    {t('??????')}
                  </Button> */}
                  <Button
                    theme='primary'
                    variant='text'
                    onClick={() => {
                      setCurrentSelection(record.row as RecommendationRuleSimpleInfo);
                      setYamlDialogVisible(true);
                    }}
                  >
                    {t('??????YAML')}
                  </Button>
                </>
              );
            },
          },
        ]}
        rowKey='index'
        selectedRowKeys={selectedRowKeys}
        hover
        onSelectChange={onSelectChange}
        pagination={{
          defaultCurrent: 1,
          defaultPageSize: 10,
          total: filterResult.length,
          showJumper: true,
          onChange(pageInfo) {
            console.log(pageInfo, 'onChange pageInfo');
          },
          onCurrentChange(current, pageInfo) {
            console.log(current, 'onCurrentChange current');
            console.log(pageInfo, 'onCurrentChange pageInfo');
          },
          onPageSizeChange(size, pageInfo) {
            console.log(size, 'onPageSizeChange size');
            console.log(pageInfo, 'onPageSizeChange pageInfo');
          },
        }}
      />
      <Dialog header={t('???????????????????????????????????????')} visible={visible} onClose={handleClose}>
        <p>{t('??????????????????API Server?????????,???????????????')}</p>
      </Dialog>
      <Dialog
        top='15vh'
        width={850}
        visible={yamlDialogVisible}
        onClose={() => {
          setYamlDialogVisible(false);
          setCurrentSelection(null);
        }}
        cancelBtn={null}
        onConfirm={() => {
          setYamlDialogVisible(false);
          setCurrentSelection(null);
        }}
      >
        <React.Suspense fallback={'loading'}>
          <Editor value={currentSelection ? toYaml(currentSelection) ?? '' : ''} />
        </React.Suspense>
      </Dialog>
    </>
  );
};

const selectPage: React.FC = () => (
  <div className={classnames(CommonStyle.pageWithPadding, CommonStyle.pageWithColor)}>
    <SelectTable />
  </div>
);

export default memo(selectPage);
