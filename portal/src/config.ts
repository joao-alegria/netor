import { environment } from "./environments/environment";

export default {
    vsEndpoint: environment.NETOR_ENDPOINT,
    login: '/tenant/oauth/token',
    whoami: '/tenant/validate',
    vsdescriptors: '/catalogue/vsdescriptor',
    vsblueprints: '/catalogue/vsblueprint',
    vsnst: '/catalogue/nstemplate',
    vsgroups: '/tenant/group',
    vstenants: '/tenant/tenant',
    vsnstemplates: '/catalogue/nst',
    vsverticalslices: '/lcm/vs',
    vsverticalslicesID: '/lcm/vs',
    vsns: '/vs/basic/nslcm/ns',
    vsdomains: '/domain/domain',
    aux1: '192.168.85.189',
    aux2: '193.136.92.69'
}