import { environment } from "./environments/environment";

export default {
    vsEndpoint: environment.NETOR_ENDPOINT,
    login: '/tenant/oauth/token',
    whoami: '/tenant/validate',
    vsdescriptors: '/vs/catalogue/vsdescriptor',
    vsblueprints: '/vs/catalogue/vsblueprint',
    vsnst: '/ns/catalogue/nstemplate',
    vsgroups: '/vs/admin/group',
    vstenants: '/vs/admin/groups/tenants',
    vsnstemplates: '/ns/catalogue/nstemplate',
    vsverticalslices: '/lcm/vs',
    vsverticalslicesID: '/lcm/vs',
    vsns: '/vs/basic/nslcm/ns',
    vsdomains: '/domainLayer/catalogue',
    aux1: '192.168.85.189',
    aux2: '193.136.92.69'
}