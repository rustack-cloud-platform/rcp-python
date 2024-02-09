from esu.paas_template import PaasTemplate
from esu.project import Project
from esu.tests import load_fixtures


@load_fixtures
def test_get_by_id(rsps):
    template_id = 1
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    template = PaasTemplate.get_object(template_id, project_id=project_id)
    assert isinstance(template, PaasTemplate)
    assert template.id == template_id
    assert template.name == 'rustack_esu_postgresql:0.1.0-SNAPSHOT'
    assert template.description == 'Some description'


@load_fixtures
def test_by_project(rsps):
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    template_id = 1
    project = Project.get_object(project_id)
    templates = project.get_paas_templates()
    assert len(templates) == 1
    template = templates[0]
    assert isinstance(template, PaasTemplate)
    assert template.id == template_id
    assert template.name == 'rustack_esu_postgresql:0.1.0-SNAPSHOT'
    assert template.description == 'Some description'
