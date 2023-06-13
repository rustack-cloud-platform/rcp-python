import pytest

from esu.base import BaseAPI, NotFoundEx
from esu.image import File, Image
from esu.tests import load_fixtures
from esu.vdc import Vdc
from esu.vm import Vm


@load_fixtures
def test_not_found_by_id(rsps):
    image = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        Image.get_object(image)


@load_fixtures
def test_get_by_id(resp):
    image = Image().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')

    assert isinstance(image, Image)
    assert image.id == 'f01776bb-968b-4b8f-835c-669535a9d0eb'
    assert image.name == 'New_Image'
    assert len(image.files) == 2


@load_fixtures
def test_create_from_vm(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vdc = Vdc.get_object(vdc_id)
    vm = Vm.get_object(vm_id)

    image = Image(name="Test_Image", vdc=vdc)
    image.create_from_vm(vm=vm)

    assert image.id
    assert image.name == "Test_Image"
    assert image.vdc.id == vdc_id


@load_fixtures
def test_create_for_upload(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)
    image = Image(name="Test_Image", vdc=vdc, type="iso")
    image.create_for_upload()

    assert image.id
    assert image.name == "Test_Image"
    assert image.vdc.id == vdc_id
    assert image.type == "iso"


@load_fixtures
def test_get_upload_link(rsps):
    image = Image(id="f01776bb-968b-4b8f-835c-669535a9d0eb", name="Test_Image",
                  type="iso")
    url = image.get_upload_link()

    assert "/proxy/ed32f09e3c94015149ff43fb7dacdc60/" in url
    assert BaseAPI.endpoint_url in url


@load_fixtures
def test_commit_upload(rsps):
    image = Image(id="f01776bb-968b-4b8f-835c-669535a9d0eb")
    image.commit_upload()

    assert image.id == "f01776bb-968b-4b8f-835c-669535a9d0eb"
    assert len(image.files) == 1


@load_fixtures
def test_get_download_link(rsps):
    file = File(name="file", type="iso", size=1,
                id="f01776bb-968b-4b8f-835c-669535a9d0de")
    image = Image(id="f01776bb-968b-4b8f-835c-669535a9d0eb")

    url = image.get_download_link(file=file)

    assert BaseAPI.endpoint_url in url
    assert "/proxy/f7f3aab95f003f0160bab00788084ef7/file.iso" in url


@load_fixtures
def test_rename(rsps):
    image = Image().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    assert image.name == 'New_Image'

    image.name = "Image_Renamed"
    image.save()

    assert image.name == "Image_Renamed"


@load_fixtures
def test_deploy_vm_from_image(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)

    image = Image().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    new_vm = image.deploy_vm_from_image(vm=vm)

    assert new_vm.name == vm.name
    assert new_vm.cpu == vm.cpu
    assert new_vm.vdc.id == vm.vdc.id
    assert new_vm.ram == vm.ram
    assert new_vm.ports[0].network.id == vm.ports[0].network.id
    assert new_vm.disks[0].storage_profile.id == vm.disks[0].storage_profile.id


@load_fixtures
def test_delete(rsps):
    image = Image().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    image.destroy()
