script
// LoginForm.test.js
import { mount } from '@vue/test-utils';
import LoginForm from '@/components/LoginForm.vue';

describe('LoginForm', () => {
  it('renders correctly', () => {
    const wrapper = mount(LoginForm);
    expect(wrapper.html()).toMatchSnapshot();
  });

  it('validates valid input', () => {
    const wrapper = mount(LoginForm);
    wrapper.find('input[name="username"]').setValue('test');
    wrapper.find('input[name="password"]').setValue('test');
    wrapper.find('button[type="submit"]').trigger('click');
    expect(wrapper.vm.submit()).toBe(true);
  });

  it('validates invalid input', () => {
    const wrapper = mount(LoginForm);
    wrapper.find('input[name="username"]').setValue('');
    wrapper.find('input[name="password"]').setValue('');
    wrapper.find('button[type="submit"]').trigger('click');
    expect(wrapper.vm.submit()).toBe(false);
  });

  it('handles empty username', () => {
    const wrapper = mount(LoginForm);
    wrapper.find('input[name="username"]').setValue('');
    wrapper.find('input[name="password"]').setValue('test');
    wrapper.find('button[type="submit"]').trigger('click');
    expect(wrapper.vm.submit()).toBe(false);
  });

  it('handles empty password', () => {
    const wrapper = mount(LoginForm);
    wrapper.find('input[name="username"]').setValue('test');
    wrapper.find('input[name="password"]').setValue('');
    wrapper.find('button[type="submit"]').trigger('click');
    expect(wrapper.vm.submit()).toBe(false);
  });
});